pipeline {
    agent any

    environment {
        IMAGE_NAME = "saaaangho/flask-api"
        IMAGE_TAG = "v3"  // 필요 시 main 브랜치 커밋 해시로 대체 가능
        DEPLOY_USER = "rocky"
        DEPLOY_HOST = "133.186.240.62"
    }

    triggers {
        githubPush()  // GitHub Webhook 푸시 이벤트 감지
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
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
                sshagent(['shlee-test-server']) {
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

