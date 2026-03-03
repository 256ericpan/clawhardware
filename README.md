# OpenClaw Hardware Integration Monitoring

This repository provides a comprehensive dashboard for monitoring OpenClaw hardware integration projects across the open-source ecosystem.

## 🦞 What is OpenClaw?

OpenClaw is your personal AI assistant that runs on any OS and any platform. It's designed to be hardware-agnostic and can integrate with various embedded systems, IoT devices, and robotics platforms.

## 📊 Dashboard Features

The interactive dashboard (`index.html`) provides:

- **Application Categories**: Robotics, IoT, Embedded Development, Maker Projects
- **Open Source Projects**: Real-time monitoring of GitHub repositories
- **Product Links**: Direct links to hardware products used in each project
- **Star Counts & Activity**: GitHub stars and last update timestamps
- **Technology Platforms**: ESP32, Arduino, Raspberry Pi, NVIDIA Jetson, etc.
- **Tags**: Including Seeed Studio, PlatformIO, NATS, and more

## 🔍 How to Use

1. **View Live Dashboard**: Visit [https://256ericpan.github.io/clawhardware/](https://256ericpan.github.io/clawhardware/)
2. **Filter by Category**: Select application categories (Robotics, IoT, etc.)
3. **Filter by Platform**: Choose specific technology platforms
4. **Search**: Find projects by name or description
5. **Sort**: Projects are automatically sorted by GitHub stars (highest first)

## 🚀 Key Discoveries

### Seeed Studio Integration
- **XIAO ESP32-C3 Node**: Ready-to-use OpenClaw firmware for Seeed XIAO ESP32-C3 + Expansion Board (~$13 IoT peripheral)
- **Repository**: [chilu18/openclaw-esp32c3-xiao-node](https://github.com/chilu18/openclaw-esp32c3-xiao-node)
- **Product Link**: [Seeed XIAO ESP32-C3](https://www.seeedstudio.com/XIAO-ESP32C3-p-5440.html)

### Robotics Integration
- **Reachy Mini**: Active integration with Reachy Mini robotic platform
- **Repository**: [ArturSkowronski/clawd-reachy-mini](https://github.com/ArturSkowronski/clawd-reachy-mini)
- **Robotics Stack**: [tomrikert/clawbody](https://github.com/tomrikert/clawbody)

### IoT & Edge AI
- **WireClaw**: ESP32 AI agent with persistent memory and offline rule engine
- **Repository**: [M64GitHub/WireClaw](https://github.com/M64GitHub/WireClaw)
- **IOnode**: ESP32 Fleet management with NATS protocol support
- **Repository**: [M64GitHub/IOnode](https://github.com/M64GitHub/IOnode)

## 📈 Monitoring Strategy

This dashboard is updated through automated monitoring that:

1. **Scans GitHub** for OpenClaw-related repositories
2. **Categorizes projects** by application type and technology stack
3. **Extracts product links** and hardware specifications
4. **Tracks star counts** and activity metrics
5. **Updates the dashboard** with new discoveries

## 🤝 Contributing

If you have OpenClaw hardware integration projects or discover new ones, please:

1. **Star relevant repositories** to help with discovery
2. **Add product links** in your project descriptions
3. **Use consistent tags** like `openclaw`, `seeed-studio`, `esp32`, etc.
4. **Report discoveries** through GitHub issues

## 📄 License

This monitoring dashboard is provided as-is for informational purposes. Individual projects maintain their own licenses.

---

*Built with ❤️ for the OpenClaw community*