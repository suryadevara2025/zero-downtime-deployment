pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPOSITORY = 'flask-app'
        AWS_ACCOUNT_ID = '697245141888'
        IMAGE_TAG = "${BUILD_NUMBER}"
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        ECR_IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/suryadevara2025/zero-downtime-deployment.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'PYTHONPATH="$WORKSPACE" .venv/bin/python -m pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                    --build-arg APP_VERSION=${IMAGE_TAG} \
                    -t ${ECR_IMAGE}:${IMAGE_TAG} \
                    -t ${ECR_IMAGE}:latest .
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    aws ecr get-login-password \
                    --region ${AWS_REGION} | \
                    docker login \
                    --username AWS \
                    --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Docker Push') { 
           steps {
                sh '''
                    docker push ${ECR_IMAGE}:${IMAGE_TAG}
                    docker push ${ECR_IMAGE}:latest
                '''
            }
        }
        stage('Deploy Green Candidate') {
    steps {
        sshagent(credentials: ['app-server-ssh']) {
            sh '''
                ssh -o StrictHostKeyChecking=no \
                -o BatchMode=yes \
                ubuntu@172.31.1.224 \
                "bash /opt/blue-green/deploy-candidate.sh ${IMAGE_TAG} ${AWS_ACCOUNT_ID}"
            '''
        }
    }
}
       stage('Switch Traffic to Green') {
    steps {
        sshagent(credentials: ['app-server-ssh']) {
            sh '''
                ssh -o StrictHostKeyChecking=no \
                    -o BatchMode=yes \
                    ubuntu@172.31.1.224 \
                    "sudo /opt/blue-green/switch-traffic.sh green"
            '''
        }
    }
}
}

    post {
    success {
        echo 'Deployment completed successfully.'
    }

    failure {
        echo 'Deployment failed. Starting rollback to Blue.'

        sshagent(credentials: ['app-server-ssh']) {
            sh '''
                ssh -o BatchMode=yes \
                    ubuntu@$172.31.1.224 \
                    "sudo /opt/blue-green/rollback.sh blue" \
                    || echo "Automatic rollback command failed. Check Application EC2."
            '''
        }
    }

    always {
        echo 'Pipeline execution finished.'
    }
}
}
