#!/usr/bin/env python

import boto3
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
ec2 = boto3.client('ec2')

allowed_amis = { 
    'ami-d0f506b0': 'Amazon Linux',
    'ami-775e4f16': 'Redhat 7.2',
    'ami-9abea4fb': 'Ubuntu 14.04'
}

size_mappings = [
    {
        'tshirt': 'Nano',
        'size': 't2.nano',
        'cpu': 1,
        'ram': 0.5,
        'disk': 20
    },
    {
        'tshirt': 'Micro',
        'size': 't2.micro',
        'cpu': 1,
        'ram': 1,
        'disk': 20
    },
    {
        'tshirt': 'Small',
        'size': 't2.small',
        'cpu': 1,
        'ram': 2,
        'disk': 20
    },
    {
        'tshirt': 'Medium',
        'size': 't2.medium',
        'cpu': 2,
        'ram': 4,
        'disk': 30
    },
    {
        'tshirt': 'Large',
        'size': 't2.large',
        'cpu': 2,
        'ram': 8,
        'disk': 50
    },
    {
        'tshirt': 'X-Large',
        'size': 'm4.xlarge',
        'cpu': 4,
        'ram': 16,
        'disk': 100
    },
    {
        'tshirt': '2X-Large',
        'size': 'm4.2xlarge',
        'cpu': 8,
        'ram': 32,
        'disk': 200
    }
]

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route('/')
@app.route('/index')
def index():
    resp = ec2.describe_instances()
    return render_template('index.html', reservations=resp['Reservations'])

@app.route('/instance/create', methods=['GET', 'POST'])
def create():
    resp = ec2.describe_images(ImageIds=allowed_amis.keys())
    if request.method == 'GET':
        return render_template('create_instance.html',
            images=resp['Images'], 
            amis=allowed_amis, 
            size_mappings=size_mappings)
    elif request.method == 'POST':
        return "Hello World"

@app.route('/instance/view/<instance_id>')
def view_instance(instance_id):
    resp = ec2.describe_instances(InstanceIds=[instance_id])    
    return render_template('instance.html', instance=resp['Reservations'][0]['Instances'][0])

@app.route('/instance/start/<instance_id>')
def start_instance(instance_id):
    resp = ec2.start_instances(InstanceIds=[instance_id])
#    return redirect( url_for('index') )
    return redirect(redirect_url())

@app.route('/instance/stop/<instance_id>')
def stop_instance(instance_id):
    resp = ec2.stop_instances(InstanceIds=[instance_id])
    #return redirect( url_for('index') )
    return redirect(redirect_url())

@app.route('/instance/terminate/<instance_id>')
def terminate_instance(instance_id):
    resp = ec2.terminate_instances(InstanceIds=[instance_id])
    #return redirect( url_for('index') )
    return redirect(redirect_url())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
