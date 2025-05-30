pipeline {
    agent any

    environment {
        IMAGE_NAME = "saaaangho/flask-api"
        IMAGE_TAG = "v3"
        DEPLOY_USER = "rocky"
        DEPLOY_HOST = "133.186.240.62"
    }

    stages {
        stage('Docker Build') {
            steps {
                sh '''
                sudo docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "$DOCKER_PASS" | sudo docker login -u "$DOCKER_USER" --password-stdin
                    sudo docker tag $IMAGE_NAME:$IMAGE_TAG $DOCKER_USER/flask-api:$IMAGE_TAG
                    sudo docker push $DOCKER_USER/flask-api:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                sshagent(['shlee-test-server']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST '
                        sudo docker pull $DOCKER_USER/flask-api:$IMAGE_TAG &&
                        sudo docker stop flask-api || true &&
                        sudo docker rm flask-api || true &&
                        sudo docker run -d --name flask-api -p 80:80 $DOCKER_USER/flask-api:$IMAGE_TAG
                    '
                    '''
                }
            }
        }
    }
}

