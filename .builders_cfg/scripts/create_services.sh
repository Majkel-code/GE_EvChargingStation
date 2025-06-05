#!/bin/bash

set -e

# Ensure this runs as root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run create_services.sh as root"
  exit 1
fi

# Target app binary paths
CHARGER_PATH="/home/ge_run/charger-app"
VEHICLE_PATH="/home/ge_run/vehicle-app"
GUI_APP_NAME="ge-evchargingstation-gui"


# Create service file function
create_service_file() {
  local service_name=$1
  local exec_path=$2
  local description=$3

  echo "📝 Creating $service_name.service..."

  cat <<EOF > "/etc/systemd/system/${service_name}.service"
    [Unit]
    Description=$description
    After=network.target

    [Service]
    ExecStart=$exec_path
    Restart=always
    User=gecharger
    WorkingDirectory=$(dirname "$exec_path")

    [Install]
    WantedBy=multi-user.target
EOF

  echo "✔️ $service_name.service created."
}


# Create services
create_service_file "charger" "$CHARGER_PATH" "Charger App Service"
create_service_file "vehicle" "$VEHICLE_PATH" "Vehicle App Service"
# create_gui_service_file "gui" "$GUI_APP_NAME" "EV GUI App Service"

# Reload systemd and enable/start services
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reexec
systemctl daemon-reload

for svc in charger vehicle; do
  echo "🔌 Enabling and starting $svc.service"
  systemctl enable "$svc.service"
  systemctl restart "$svc.service"
done



echo "✅ All services installed and started."
