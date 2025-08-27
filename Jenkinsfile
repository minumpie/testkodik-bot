pipeline {
    agent any

    environment {
        BOT_TOKEN = credentials('BOT_TOKEN')
        DOCKER_CREDS = credentials('dockerhub')
        IMAGE_NAME = "kushogimi/testkodik_bot"
        IMAGE_TAG = "v1.1"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/minumpie/testkodik-bot.git'
            }
        }

        stage('Python Tests') {
            steps {
                sh '''
                    echo "🐍 Запускаем pytest..."
                    pip install -r requirements.txt
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Java Tests') {
            steps {
                dir('java-tests') {
                    sh '''
                        echo "☕ Запускаем юнит-тесты на Java..."
                        mvn clean test
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "🐳 Собираем Docker образ..."
                    docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin
                    docker push $IMAGE_NAME:$IMAGE_TAG
                    docker logout
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker rm -f testkodik_bot || true
                    docker run -d --name testkodik_bot \
                        -e BOT_TOKEN=$BOT_TOKEN \
                        $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
    }
}
