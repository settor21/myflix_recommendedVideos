pipeline {
    agent any

    environment {
        PROD_USERNAME = 'amedikusettor'
        PROD_SERVER = '35.239.170.49'
        PROD_DIR = '/home/amedikusettor/myflix/recommendations'
        DOCKER_IMAGE_NAME = 'recommendations-deployment'
        DOCKER_CONTAINER_NAME = 'recommendations'
        DOCKER_CONTAINER_PORT = '6001'
        DOCKER_HOST_PORT = '6001'
    }

    stages {
        stage('Load Code to Workspace') {
            steps {
                // This step automatically checks out the code into the workspace.
                checkout scm             
            }
        }

        stage('Deploy Repo to DB Server') {
            steps {
                script {
                    sh 'echo Packaging files ...'
                    sh 'rm -f movieupload_files.tar.gz || true'
                    sh 'tar -czf movieupload_files.tar.gz * || true'
                    sh "scp -o StrictHostKeyChecking=no movieupload_files.tar.gz ${PROD_USERNAME}@${PROD_SERVER}:${PROD_DIR}"
                    sh 'echo Files transferred to server. Unpacking ...'
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'pwd && cd myflix/recommendations && tar -xzf movieupload_files.tar.gz && ls -l'"
                    sh 'echo Repo unloaded on Prod. Server. Preparing to dockerize application ..'
                }
            }
        }

        stage('Dockerize ') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/recommendations && docker build -t ${DOCKER_IMAGE_NAME} .'"
                    sh "echo Docker image for Recommendations rebuilt. Preparing to redeploy container to web..."
                }
            }
        }

        stage('Redeploy Container to Web') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/recommendations && docker stop ${DOCKER_CONTAINER_NAME} || echo \"Failed to stop container\"'"
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/recommendations && docker rm ${DOCKER_CONTAINER_NAME} || echo \"Failed to remove container\"'"
                    sh "echo Container stopped and removed. Preparing to redeploy new version"

                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/recommendations && docker run -d -p ${DOCKER_HOST_PORT}:${DOCKER_CONTAINER_PORT} --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE_NAME}'"
                    sh "echo Recommendations script Deployed!"
                }
            }
        }
    }
}
