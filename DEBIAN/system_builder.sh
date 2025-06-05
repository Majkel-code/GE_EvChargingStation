#!/bin/bash
set -e

# === Configuration ===
IMG_NAME="builder_enablesshgen2clenup_keygen.img"
IMG_SIZE_MB=4096
COMPRESSED_IMG="${IMG_NAME}.xz"
MOUNT_ROOT="/mnt/clone-root"
MOUNT_BOOT="/mnt/clone-boot"
FIRMWARE_SRC="/boot/firmware"

# === Cleanup previous mounts and images if present ===
echo "==> Cleaning up any previous runs..."
losetup -D
umount "$MOUNT_ROOT" 2>/dev/null || true
umount "$MOUNT_BOOT" 2>/dev/null || true
rm -f "$IMG_NAME" "$COMPRESSED_IMG"
rm -rf "$MOUNT_ROOT" "$MOUNT_BOOT"
mkdir -p "$MOUNT_BOOT" "$MOUNT_ROOT"

# === Create blank image ===
echo "==> Creating blank image..."
USED_BYTES=$(df --output=used -B1 / | tail -n1)
BUFFER=$((2 * 1024 * 1024 * 1024))  # 2GB buffer
IMG_SIZE=$((USED_BYTES + BUFFER))

echo "[*] Creating image of size $((IMG_SIZE / 1024 / 1024)) MB"
dd if=/dev/zero of="$IMG_NAME" bs=1 count=0 seek=$IMG_SIZE

# === Partition image ===
echo "==> Partitioning image..."
parted -s "$IMG_NAME" mklabel msdos
parted -s "$IMG_NAME" mkpart primary fat32 1MiB 256MiB
parted -s "$IMG_NAME" set 1 boot on
parted -s "$IMG_NAME" mkpart primary ext4 256MiB 100%

# === Setup loop device ===
echo "==> Attaching loop device..."
loopdev=$(losetup --find --partscan --show "$IMG_NAME")
bootdev="${loopdev}p1"
rootdev="${loopdev}p2"

# === Format partitions ===
echo "==> Formatting partitions..."
mkfs.vfat -F 32 -n BOOT "$bootdev"
mkfs.ext4 -L rootfs "$rootdev"

# === Mount partitions ===
echo "==> Mounting image..."
mount "$bootdev" "$MOUNT_BOOT"
mount "$rootdev" "$MOUNT_ROOT"

# === Copy root filesystem ===
echo "==> Copying root filesystem..."
rsync -aAXv \
  --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found","/home/gecharger/addons/*"} \
  / "$MOUNT_ROOT"

echo "==> Creating empty /home/gecharger..."
mkdir -p "$MOUNT_ROOT/home/gecharger"
chown --reference=/home/gecharger "$MOUNT_ROOT/home/gecharger"
chmod --reference=/home/gecharger "$MOUNT_ROOT/home/gecharger"
mkdir -p "$MOUNT_ROOT/home/gecharger/addons"
chown --reference=/home/gecharger "$MOUNT_ROOT/home/gecharger/addons"
chmod --reference=/home/gecharger "$MOUNT_ROOT/home/gecharger/addons"

# === Copy boot files and create /boot/firmware compatibility ===
echo "==> Copying boot partition from $FIRMWARE_SRC..."
rsync -aAXv "$FIRMWARE_SRC"/ "$MOUNT_BOOT"

echo "==> Creating /boot/firmware compatibility directory..."
mkdir -p "$MOUNT_BOOT/firmware"
rsync -aAXv "$MOUNT_BOOT"/ "$MOUNT_BOOT/firmware/" --exclude=firmware


# === Enable SSH on first boot ===
echo "==> Enabling SSH..."
touch "$MOUNT_BOOT/ssh"

# === Fix cmdline and fstab ===
echo "==> Updating cmdline.txt and fstab..."
sed -i 's|root=PARTUUID=[^ ]*|root=/dev/mmcblk0p2|' "$MOUNT_BOOT/cmdline.txt"

cat <<EOF > "$MOUNT_ROOT/etc/fstab"
/dev/mmcblk0p1  /boot vfat defaults  0 2
/dev/mmcblk0p2  /     ext4 defaults,noatime  0 1
EOF

# === Clean SSH keys and machine ID ===
echo "==> Cleaning SSH host keys and machine ID..."
rm -f "$MOUNT_ROOT/etc/ssh/ssh_host_*"
rm -f "$MOUNT_ROOT/etc/machine-id"
touch "$MOUNT_ROOT/etc/machine-id"

rm -f "$MOUNT_ROOT/var/lib/systemd/random-seed"
rm -f "$MOUNT_ROOT/var/lib/systemd/ssh-keygen.service"

# === Enable SSH keygen services ===
echo "==> Setting up SSH key regeneration with systemd..."
chroot "$MOUNT_ROOT" systemctl enable ssh.service

# # === Add root filesystem expansion on first boot ===
# --- Create the resize script ---
cat << 'EOF' > "$MOUNT_ROOT/usr/local/bin/resize-rootfs.sh"
#!/bin/bash
set -e

echo "[resize-rootfs] Growing partition on first boot..."

ROOT_PART=$(findmnt / -o SOURCE -n)
DEV=$(echo "$ROOT_PART" | sed -E 's/p?[0-9]+$//')

parted "$DEV" ---pretend-input-tty <<EOPART
resizepart
2
Yes
100%
EOPART

sleep 5
resize2fs "$ROOT_PART"

systemctl disable resize-rootfs.service
EOF

chmod +x "$MOUNT_ROOT/usr/local/bin/resize-rootfs.sh"

# --- Create the systemd unit ---
mkdir -p "$MOUNT_ROOT/etc/systemd/system"
cat << EOF > "$MOUNT_ROOT/etc/systemd/system/resize-rootfs.service"
[Unit]
Description=Resize root filesystem on first boot
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/resize-rootfs.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

# --- Enable it ---
ln -sf ../resize-rootfs.service "$MOUNT_ROOT/etc/systemd/system/multi-user.target.wants/resize-rootfs.service"

echo "✅ resize-rootfs service injected successfully."



# === Finalize ===
echo "==> Unmounting and detaching..."
sync
umount "$MOUNT_BOOT"
umount "$MOUNT_ROOT"
losetup -d "$loopdev"

# === Compress image ===
echo "==> Compressing image..."
xz -T0 -6 "$IMG_NAME" 

echo "✅ Compressed image created: $COMPRESSED_IMG"

# === Final cleanup ===
echo "==> Final cleanup..."
rm -rf "$MOUNT_BOOT" "$MOUNT_ROOT"
losetup -D