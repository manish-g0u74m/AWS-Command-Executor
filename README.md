# 🌩️ AWS Command Executor

![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)

AWS Command Executor is a Flask-based web application that allows users to execute various AWS commands through a simple web interface. Users can list EC2 instances, get their AWS account ID, find the latest Amazon Linux AMI ID in the Mumbai region, and more.

## ✨ Features

- 📋 List EC2 instances in the selected region.
- 🔍 Retrieve AWS account ID.
- 🌐 Get the total number of active availability zones in the Mumbai region.
- 🆕 Find the latest Amazon Linux AMI ID in the Mumbai region.
- 🛑 Stop all running instances in the Mumbai region.
- 🔐 Create a security group in the Mumbai region.
- 🔑 Create an SSH key pair in the Mumbai region.
- 🚀 Launch an EC2 instance with the latest Amazon Linux AMI in the Mumbai region.
- 💰 Get the total pending account bill for the last month in USD.

## 🛠️ Dependencies

- 🐍 Python 3.x
- 🌶️ Flask
- 🐳 boto3 (AWS SDK for Python)

## 📥 Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/manish-g0u74m/AWS-Command-Executor.git
    cd AWS-Command-Executor
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\\Scripts\\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    Ensure your `requirements.txt` includes:
    ```
    Flask
    boto3
    ```

4. **Set up your AWS credentials:**

    Ensure you have your AWS Access Key ID and Secret Access Key ready.

5. **Run the application:**

    ```bash
    python app.py
    ```

6. **Open your web browser and navigate to:**

    ```
    http://127.0.0.1:5000/
    ```

## 🚀 Usage

1. **Enter your AWS Access ID and Secret Key.**
2. **Enter the desired prompt commands, one per line.**
3. **Click "Execute Commands" to run the AWS commands and view the results.**

## 📝 Example Prompts
These Prompts are Used in the Application You can simply copy and paste them One by One
- `list ec2 instances`
- `my aws account id`
- `total active az in mumbai aws`
- `latest amazon linux ami id in mumbai region`
- `stop all instance running in mumbai region`
- `create security group in aws name manishsg in mumbai region`
- `create ssh key pair name manishkey in aws mumbai region`
- `launch ec2 instance with latest amazon linux ami in mumbai region without key pair and without security group`
- `total pending account bill of aws of last 1 month in usd`

## 📁 Project Structure

- `app.py`: Main Flask application.
- `templates/index.html`: Main HTML template for the web interface.
- `templates/output.html`: Main HTML template for the web interface output.
- `static/scripts.js`: JavaScript for handling form submissions and interactions.
- `static/styles.css`: CSS for styling the web interface.

## 🤝 Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgements

- Thanks to the open-source community for the tools and resources that made this project possible.
- Special thanks to the Flask and boto3 libraries for their robust functionality and ease of use.

