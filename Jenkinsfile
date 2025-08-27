pipeline {
    agent any

    environment {
        BOT_TOKEN = credentials('BOT_TOKEN')       // секретный токен бота
        DOCKER_CREDS = credentials('dockerhub')    // логин+пароль для Docker Hub
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
                    echo "🔐 Логинимся в Docker Hub..."
                    echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin

                    echo "📤 Публикуем образ в Docker Hub..."
                    docker push $IMAGE_NAME:$IMAGE_TAG

                    docker logout
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    echo "🚀 Запускаем контейнер..."
                    docker rm -f testkodik_bot || true
                    docker run -d --name testkodik_bot \
                        -e BOT_TOKEN=$BOT_TOKEN \
                        $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
    }
}
