# 💊 MicroClinic Plus Pharmacy Manager

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/github/license/WabukoWabuko/MicroClinicPlusPharmacyManager)

## 📋 Overview
**MicroClinic Plus Pharmacy Manager** is a desktop application built with **PyQt6** to streamline core pharmacy operations — from patient and inventory management to sales and reporting. It features a modular interface, real-time status updates, and accessibility options.

---

## 🚀 Features

- 🔐 **Login System** – Secure authentication with username and password.
- 📂 **Modular Menu** – Navigate through Patient, Inventory, Sales, and more.
- 🌐 **Dynamic Status** – Auto-checks online/offline state every 5 seconds.
- 🌓 **High Contrast Mode** – Toggle accessibility mode on demand.
- 💬 **Inspirational Quotes** – Health quotes rotate every minute on login.
- 🗄️ **Database Integration** – Persistent storage with config management.

---

## 🛠️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/WabukoWabuko/MicroClinicPlusPharmacyManager.git
   cd MicroClinicPlusPharmacyManager
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install PyQt6
   ```
4. Ensure the `database/logo.png` file is present or update the path in `ui/login.py`.

## Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. Log in with valid credentials (configured via `db.database`).
3. Navigate the menu to access different modules.

## Project Structure
```mermaid
graph TD
    A[💊 MicroClinic Plus: Pharmacy Manager] --> B[🪟 Main Window]
    A --> C[🗄️ Database Layer]
    
    B --> D[🔐 Login Widget]
    B --> E[📂 Main Menu]

    E --> F[🧑‍⚕️ Patient Management]
    E --> G[📦 Inventory Management]
    E --> H[📝 Prescription Logging]
    E --> I[💰 Sales Management]
    E --> J[🚚 Supplier Management]
    E --> K[🛡️ User Management\n(Admin Only)]
    E --> L[⚙️ Settings]
    E --> M[📊 Reporting Dashboard]

    C --> N[🔑 Authenticate User]
    C --> O[📁 Load Config]
    C --> P[🌐 Check Connectivity]
```

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Description"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For issues or suggestions, please open an issue on the GitHub repository or contact the maintainer at basilwabbs@gmail.com.
