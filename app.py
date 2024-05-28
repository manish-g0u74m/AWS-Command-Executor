from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

AWS_REGION = 'ap-south-1'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    aws_access_id = request.form['access_id']
    aws_secret_key = request.form['secret_key']
    prompts = request.form['prompts'].split('\n')

    session = boto3.Session(
        aws_access_key_id=aws_access_id,
        aws_secret_access_key=aws_secret_key,
        region_name=AWS_REGION
    )

    ec2_client = session.client('ec2')
    sts_client = session.client('sts')
    billing_client = session.client('ce')

    outputs = []

    for prompt in prompts:
        if prompt.strip().lower() == 'list ec2 instances':
            instances = ec2_client.describe_instances()
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    outputs.append(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")

        elif prompt.strip().lower() == 'my aws account id':
            account_id = sts_client.get_caller_identity()['Account']
            outputs.append(f"AWS Account ID: {account_id}")

        elif prompt.strip().lower() == 'total active az in mumbai aws':
            az_count = len(ec2_client.describe_availability_zones()['AvailabilityZones'])
            outputs.append(f"Total Active Availability Zones in Mumbai: {az_count}")

        elif prompt.strip().lower() == 'latest amazon linux ami id in mumbai region':
            images = ec2_client.describe_images(
                Owners=['amazon'],
                Filters=[
                    {'Name': 'name', 'Values': ['amzn2-ami-hvm-*']},
                    {'Name': 'architecture', 'Values': ['x86_64']},
                    {'Name': 'root-device-type', 'Values': ['ebs']},
                    {'Name': 'virtualization-type', 'Values': ['hvm']},
                    {'Name': 'state', 'Values': ['available']}
                ]
            )
            if images['Images']:
                latest_image_id = max(images['Images'], key=lambda x: x['CreationDate'])['ImageId']
                ami_description = ec2_client.describe_images(ImageIds=[latest_image_id])
                for image in ami_description['Images']:
                    outputs.append(f"Latest Amazon Linux AMI ID in Mumbai Region: {latest_image_id}, Region: {AWS_REGION}, Name: {image['Name']}")
            else:
                outputs.append("No Amazon Linux AMI found in Mumbai Region")



        elif prompt.strip().lower() == 'stop all instance running in mumbai region':
            instances = ec2_client.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    region = instance['Placement']['AvailabilityZone'][:-1]  # Extract region from AZ
                    if region == 'ap-south-1':  # Mumbai Region
                        ec2_client.stop_instances(InstanceIds=[instance_id])
                        outputs.append(f"Stopped Instance ID: {instance_id}")

        elif prompt.strip().lower() == 'create security group in aws name manishsg in mumbai region':
            try:
                sg_response = ec2_client.create_security_group(
                    GroupName='manishsg',
                    Description='Security group for SSH access',
                    VpcId='vpc-0d2b9dc4e3d2e0585'  # Replace with your VPC ID
                )
                sg_id = sg_response['GroupId']
                ec2_client.authorize_security_group_ingress(
                    GroupId=sg_id,
                    IpPermissions=[
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        }
                    ]
                )
                outputs.append("Security group 'manishsg' created successfully.")
            except Exception as e:
                outputs.append(f"Error creating security group: {str(e)}")

        elif prompt.strip().lower() == 'create ssh key pair name manishkey in aws mumbai region':
            try:
                key_pair = ec2_client.create_key_pair(KeyName='manishkey')
                key_material = key_pair['KeyMaterial']
                with open('C:/Users/g0u74m/Desktop/manishkey.pem', 'w') as f:
                    f.write(key_material)
                outputs.append("SSH key pair 'manishkey' created successfully.")
            except Exception as e:
                outputs.append(f"Error creating SSH key pair: {str(e)}")

        elif prompt.strip().lower() == 'launch ec2 instance with latest amazon linux ami in mumbai region without key pair and without security group':
            try:
                response = ec2_client.run_instances(
                    ImageId='ami-0cc9838aa7ab1dce7',  # Replace with the latest Amazon Linux AMI ID
                    InstanceType='t2.micro',  # Replace with desired instance type
                    MaxCount=1,
                    MinCount=1
                )
                instance_id = response['Instances'][0]['InstanceId']
                outputs.append(f"EC2 instance with Instance ID '{instance_id}' launched successfully.")
            except Exception as e:
                outputs.append(f"Error launching EC2 instance: {str(e)}")

        elif prompt.strip().lower() == 'total pending account bill of aws of last 1 month in usd':
            try:
                import datetime
                end = datetime.datetime.utcnow()
                start = end - datetime.timedelta(days=30)
                cost_response = billing_client.get_cost_and_usage(
                    TimePeriod={
                        'Start': start.strftime('%Y-%m-%d'),
                        'End': end.strftime('%Y-%m-%d')
                    },
                    Granularity='MONTHLY',
                    Metrics=['UnblendedCost']
                )
                total_cost = cost_response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
                currency = cost_response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit']
                outputs.append(f"Total pending account bill of AWS for last 1 month: {total_cost} {currency}")
            except Exception as e:
                outputs.append(f"Error fetching account bill: {str(e)}")

    return render_template('output.html', outputs=outputs)

if __name__ == '__main__':
    app.run(debug=True)
