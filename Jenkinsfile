pipeline {
    agent any

    environment {

    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Git Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/stwins60/policy-sentry.git'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    dir('./k8s') {
                        kubeconfig(credentialsId: '500a0599-809f-4de0-a060-0fdbb6583332', serverUrl: '') {
                            def targetEnvironment = determineTargetEnvironment()
                            sh "kubectl apply -f ${targetEnvironment}-deployment.yaml"
                            sh "kubectl apply -f ${targetEnvironment}-svc.yaml"
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