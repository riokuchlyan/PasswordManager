# Password Manager README

## Overview
Welcome to the **Password Manager** – a secure, local alternative to cloud-based password management solutions. Developed in Python using the Tkinter GUI framework and robust encryption libraries, this application offers a reliable solution for storing and managing passwords directly on your Mac without relying on the cloud. This Password Manager is especially suited for users who prioritize privacy and local storage over cloud-based options. 

With this tool, you can securely store passwords, generate strong new ones, and manage your credentials in an encrypted, password-protected CSV file, ensuring that sensitive data is safe from unauthorized access.

---

## Features
- **Secure Local Storage:** Stores passwords locally on your macOS in an encrypted CSV file, providing privacy and security without relying on cloud storage.
- **Password Encryption:** Uses industry-standard encryption algorithms to ensure your data remains protected. Only accessible by entering a master password.
- **Password Generation:** Generates strong passwords to enhance the security of your online accounts.
- **Export Options:** Allows you to export your stored passwords to an unencrypted CSV file if you need them in plain text for backup or other purposes.
- **User-Friendly Interface:** Built with Python's Tkinter, the graphical interface is simple, intuitive, and easy to navigate for all users.

---

## Installation Instructions
### Prerequisites
This Password Manager is currently available only on **macOS**. Ensure that you have the following:
- macOS (tested on macOS 10.15 and above)
- Python 3.8 or later (if you want to run the source code)
  
### Installation Steps
1. **Download the .dmg file**:
   - Visit the [Password Manager release page] and download the latest `.dmg` file.
2. **Install the Application**:
   - Open the downloaded `.dmg` file.
   - Drag the Password Manager application icon to your Applications folder.
3. **Open the Application**:
   - Locate the Password Manager in your Applications folder.
   - Double-click to open it. If macOS warns that it’s an application downloaded from the internet, you may need to go to **System Preferences > Security & Privacy** and allow it to open.

---

## Usage
### Initial Setup
1. **Open the Password Manager** by double-clicking on the application icon.
2. **Set a Master Password**: The first time you launch the app, you’ll be prompted to set a master password. This password is essential, as it’s used to encrypt and decrypt your stored data.
3. **Creating Entries**:
   - Enter the website, username, and password for each account you want to save.
   - Use the built-in **Password Generator** for creating strong, secure passwords if you don’t already have one.
   - Click **Save** to add the entry to your encrypted storage file.

### Managing Entries
- **View Saved Passwords**: Enter your master password to decrypt and view your saved entries. The list of passwords will display only within the app interface.
- **Export Passwords**: To back up your data, you can export passwords to an unencrypted CSV file. This file will be saved in plain text format for easy access, so use caution and store it securely.
  
### Password Generation
- Select **Generate Password** to create a random, strong password. Options allow you to adjust length and complexity, including uppercase, lowercase, numbers, and special characters.

---

## Security Considerations
- **Local Storage**: All passwords are stored locally on your Mac, not in the cloud.
- **Encrypted Data**: Passwords are stored in an encrypted format. Without the master password, the data cannot be accessed, providing an extra layer of security.
- **Master Password**: Ensure that you remember your master password. If it’s lost, the encrypted data cannot be recovered.
- **Exported CSV**: Any passwords exported to an unencrypted CSV file are in plain text. Store this file securely or delete it after use to prevent unauthorized access.

---

## Troubleshooting
### Cannot Open Application
- If macOS blocks the app from opening, check **System Preferences > Security & Privacy** to allow it.

### Forgotten Master Password
- The master password is crucial for accessing encrypted data. If forgotten, there is no way to recover it, as the data is securely encrypted.

### Exported CSV Issues
- Ensure the exported file is stored securely. Unencrypted CSV files are vulnerable to unauthorized access.

---

## Future Improvements
Planned enhancements for future releases may include:
- Compatibility with Windows and Linux systems
- Biometric or two-factor authentication
- Enhanced password auditing tools for assessing the strength and usage of saved passwords
- Synchronization with other devices, keeping data storage entirely offline

---

## Contributing
If you’d like to contribute, please reach out with ideas, or consider submitting a pull request (source code available soon). Your feedback and suggestions are always welcome.

---

## License
This project is released under the GPL-3.0 License. Please refer to the [LICENSE](./LICENSE) file for more details.

---

Thank you for choosing **Password Manager**! If you have any questions or feedback, please feel free to reach out.
