pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('d4506f04-b98c-47db-95ce-018ceac27ba6')
        BRANCH_NAME = "${GIT_BRANCH.split("/")[1]}"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Git Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/dev'], [name: '*/qa'], [name: '*/prod']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/stwins60/policy-sentry.git']])
            }
        }

        stage("Docker Login") {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                echo "Login Succeeded"
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    def imageTag = determineTargetEnvironment()
                    sh "docker build -t idrisniyi94/policy-sentry:${imageTag} ."
                }
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    def imageTag = determineTargetEnvironment()
                    sh "docker push idrisniyi94/policy-sentry:${imageTag}"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    dir('./k8s') {
                        kubeconfig(credentialsId: '500a0599-809f-4de0-a060-0fdbb6583332', serverUrl: '') {
                            def targetEnvironment = determineTargetEnvironment()
                            sh "kubectl apply -f ${targetEnvironment}-deployment.yaml"
                            sh "kubectl apply -f ${targetEnvironment}-service.yaml"
                        }
                    }
                }
            }
        }
        
    }
}

def determineTargetEnvironment() {
    def branchName = env.BRANCH_NAME
    if (branchName == 'qa') {
        return 'qa'
    } else if (branchName == 'prod') {
        return 'prod'
    } else {
        return 'dev'
    }
}