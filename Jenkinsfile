pipeline {
    agent any

    environment {
        PROD_USERNAME = 'amedikusettor'
        PROD_SERVER = '35.239.170.49'
        PROD_DIR = '/home/amedikusettor/myflix/recommendations'
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
                    sh 'rm -f recommendation_files.tar.gz || true'
                    sh 'tar -czf recommendation_files.tar.gz * || true'
                    sh "scp -o StrictHostKeyChecking=no recommendation_files.tar.gz ${PROD_USERNAME}@${PROD_SERVER}:${PROD_DIR}"
                    sh 'echo Files transferred to server. Unpacking ...'
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'cd myflix/recommendations && tar -xzf recommendation_files.tar.gz && ls -l'"
                    sh 'echo Repo unloaded on Prod. Server. Preparing to install libraries ..'
                }
            }
        }

        stage('Install Libraries') {
            steps {
                script {
                    // Add commands to install necessary libraries on the server
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'sudo apt-get update && sudo apt-get install -y python3-pip'"
                    sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'pip3 install pymongo neo4j-driver pytz'"
                    sh "echo Libraries installed. Preparing to create cron job for recommendations.py"
                }
            }
        }
        stage('Create Cron Job') {
            steps {
                script {
                    // Check if the cron job already exists
                    def cronExists = sh(script: "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} 'crontab -l | grep -q \"${PROD_DIR}\"'", returnStatus: true) == 0

                    if (!cronExists) {
                        // Add commands to create a cron job
                        sh "ssh -o StrictHostKeyChecking=no ${PROD_USERNAME}@${PROD_SERVER} '(crontab -l ; echo \"0 5 * * * cd ${PROD_DIR} && /usr/bin/python3 recommendations.py\") | crontab -'"
                        echo "Cron job for recommendations.py created!"
        
                    } else {
                        echo "Cron job already exists. Skipping creation."
                    }
                    echo "Neo4J script for generating recommendations deployed"
                }
            }
        }      
    }
}