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
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker tag $IMAGE_NAME:$IMAGE_TAG $DOCKER_USER/flask-api:$IMAGE_TAG
                    docker push $DOCKER_USER/flask-api:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                sshagent(credentials: ['shlee']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST '
                        docker pull $DOCKER_USER/flask-api:$IMAGE_TAG &&
                        docker stop flask-api || true &&
                        docker rm flask-api || true &&
                        docker run -d --name flask-api -p 80:80 $DOCKER_USER/flask-api:$IMAGE_TAG
                    '
                    '''
                }
            }
        }
    }
}

