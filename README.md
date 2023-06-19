<div align="center">
<img src="/logo.svg" width="50%"></img>
<br/><br/>
<i>Made for developers by a developer.</i>
</div>
<br/>

Terminal TOTP Manager is a command-line tool for managing Time-based One-Time Passwords (TOTPs). <br/>It allows you to securely store and generate TOTPs for your various accounts.

## Prerequisites

- Python 3.x
- Required dependencies: `pycryptodome`

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies by running the following command:
   ```
   pip install pycryptodome
   ```

## Usage

To use TOTP Manager, follow these steps:

    1. Open a terminal or command prompt and navigate to the project directory.

    2. Run the following command:

   ```
   python app.py [command]
   ```

   Replace `[command]` with one of the following options:

   - `add`: Add a new TOTP credential.
   - `list`: List all saved TOTPs
   - `delete`: Delete a TOTP credential.

3. If this is your first time using TOTP Manager, you will be prompted to create a password to secure your credentials. The password must be at least 8 characters long.

4. Depending on the command you choose:

   - For `add`: You can enter the OTPauth URI directly or provide the required information manually.
   - For `list`: The Issuer and their associated TOTPs will be displayed continuously.
   - For `delete`: Select the issuer of the credential you want to delete from the displayed list.

## Security

- The TOTP Manager stores your credentials securely by hashing the password before storing it in a JSON file (`db.json`).
- You can only access the TOTP Manager by providing the correct password.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please report them on the project's GitHub page.

## License

The Project is released under the [MIT License](https://opensource.org/licenses/MIT). Please refer to the LICENSE file for more details.
