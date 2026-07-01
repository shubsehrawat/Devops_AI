TEST_QUERIES = [
    {
        "id": 1,
        "query": "Why did the Payment API fail yesterday?",
        "intent": "rca",
        "expected_documents": [
            "RCA-001_Payment_API_Timeout_Due_to_Database_Connection_Pool_Exhaustion.pdf"
        ],
        "ground_truth": """
The Payment API outage was caused by database connection pool exhaustion.
The exhausted connection pool prevented new database connections from being established, resulting in request timeouts.
The issue impacted customer payment transactions and caused SLA violations.
The engineering team restored service by optimizing the connection pool configuration and validating application stability through monitoring.
"""
    },

    {
        "id": 2,
        "query": "Why were Kubernetes pods evicted?",
        "intent": "rca",
        "expected_documents": [
            "RCA-002_Kubernetes_Node_Failure_Causing_Pod_Evictions.pdf"
        ],
        "ground_truth": """
Pods were evicted because a Kubernetes worker node became unhealthy.
The scheduler redistributed workloads after the node failure, causing temporary service disruption.
The affected node was recovered and workloads were successfully rescheduled.
"""
    },

    {
        "id": 3,
        "query": "Why did authentication suddenly fail?",
        "intent": "rca",
        "expected_documents": [
            "RCA-003_Redis_Memory_Exhaustion_Leading_to_Authentication_Failures.pdf"
        ],
        "ground_truth": """
Authentication requests failed because Redis exhausted its available memory.
Session data could no longer be stored, resulting in authentication failures.
The Redis cache was cleaned, memory limits were adjusted, and service stability was restored.
"""
    },

    {
        "id": 4,
        "query": "Why did Jenkins deployment fail?",
        "intent": "rca",
        "expected_documents": [
            "RCA-004_Jenkins_Pipeline_Failure_Due_to_Expired_Service_Principal.pdf"
        ],
        "ground_truth": """
The Jenkins deployment failed because the Azure Service Principal used by the pipeline had expired.
After renewing the credentials and updating the pipeline secrets, deployments completed successfully.
"""
    },

    {
        "id": 5,
        "query": "Why was production unavailable because of SSL?",
        "intent": "rca",
        "expected_documents": [
            "RCA-005_SSL_Certificate_Expiry_Causing_Production_Outage.pdf"
        ],
        "ground_truth": """
Production became unavailable because the SSL certificate expired.
Clients were unable to establish secure HTTPS connections.
Renewing the certificate and updating the load balancer restored service.
"""
    },

    {
        "id": 6,
        "query": "Give me the Kubernetes deployment runbook.",
        "intent": "runbook",
        "expected_documents": [
            "RB-001_Kubernetes_Deployment_Runbook.pdf"
        ],
        "ground_truth": """
The Kubernetes deployment runbook includes prerequisites, deployment steps, verification procedures, rollback instructions, and post-deployment validation.
"""
    },

    {
        "id": 7,
        "query": "How do I restart the Payment API?",
        "intent": "runbook",
        "expected_documents": [
            "RB-002_Payment_API_Restart_Runbook.pdf"
        ],
        "ground_truth": """
The runbook describes the process for restarting the Payment API, validating application health, checking logs, and confirming successful recovery.
"""
    },

    {
        "id": 8,
        "query": "Show me the Redis maintenance runbook.",
        "intent": "runbook",
        "expected_documents": [
            "RB-003_Redis_Maintenance_Runbook.pdf"
        ],
        "ground_truth": """
The Redis maintenance runbook covers backup procedures, maintenance windows, restart operations, health verification, and rollback steps.
"""
    },

    {
        "id": 9,
        "query": "Provide the Jenkins deployment runbook.",
        "intent": "runbook",
        "expected_documents": [
            "RB-004_Jenkins_Deployment_Runbook.pdf"
        ],
        "ground_truth": """
The Jenkins deployment runbook provides deployment prerequisites, execution steps, pipeline validation, rollback procedures, and deployment verification.
"""
    },

    {
        "id": 10,
        "query": "How do I rotate SSL certificates?",
        "intent": "runbook",
        "expected_documents": [
            "RB-005_SSL_Certificate_Rotation_Runbook.pdf"
        ],
        "ground_truth": """
The SSL certificate rotation runbook explains certificate renewal, installation, validation, load balancer updates, and rollback procedures.
"""
    },

    {
        "id": 11,
        "query": "Summarize incident INC-001.",
        "intent": "incident_summary",
        "expected_documents": [
            "INC-001.pdf"
        ],
        "ground_truth": """
Provide a concise summary including the incident timeline, affected services, business impact, actions taken, current status, and lessons learned.
"""
    },

    {
        "id": 12,
        "query": "Give me the summary of incident INC-002.",
        "intent": "incident_summary",
        "expected_documents": [
            "INC-002.pdf"
        ],
        "ground_truth": """
Summarize the incident, highlighting root cause, impacted systems, mitigation actions, and final resolution.
"""
    },

    {
        "id": 13,
        "query": "Explain incident INC-003.",
        "intent": "incident_summary",
        "expected_documents": [
            "INC-003.pdf"
        ],
        "ground_truth": """
Summarize the complete incident including timeline, impact, engineering response, resolution, and preventive actions.
"""
    },

    {
        "id": 14,
        "query": "How do I troubleshoot CrashLoopBackOff?",
        "intent": "troubleshooting",
        "expected_documents": [
            "TS-001_CrashLoopBackOff_Troubleshooting_Guide.pdf"
        ],
        "ground_truth": """
Troubleshooting steps should include checking pod logs, describing the pod, verifying resource limits, examining Kubernetes events, and validating container configuration.
"""
    },

    {
        "id": 15,
        "query": "How do I fix a database connection timeout?",
        "intent": "troubleshooting",
        "expected_documents": [
            "TS-002_Database_Timeout_Troubleshooting.pdf"
        ],
        "ground_truth": """
Investigate database connectivity, verify connection pools, review database logs, inspect network latency, and validate application configuration.
"""
    },

    {
        "id": 16,
        "query": "Troubleshoot Jenkins pipeline failure.",
        "intent": "troubleshooting",
        "expected_documents": [
            "TS-003_Jenkins_Pipeline_Troubleshooting.pdf"
        ],
        "ground_truth": """
Troubleshooting should include pipeline log analysis, credential verification, plugin validation, and agent connectivity checks.
"""
    },

    {
        "id": 17,
        "query": "Show me the production deployment SOP.",
        "intent": "sop",
        "expected_documents": [
            "SOP-001_Production_Deployment.pdf"
        ],
        "ground_truth": """
The Production Deployment SOP describes approval workflow, deployment steps, validation checks, rollback procedures, and post-deployment monitoring.
"""
    },

    {
        "id": 18,
        "query": "Database backup SOP.",
        "intent": "sop",
        "expected_documents": [
            "SOP-002_Database_Backup.pdf"
        ],
        "ground_truth": """
The Database Backup SOP explains backup scheduling, verification, retention policy, restoration testing, and compliance requirements.
"""
    },

    {
        "id": 19,
        "query": "Disaster recovery SOP.",
        "intent": "sop",
        "expected_documents": [
            "SOP-003_Disaster_Recovery.pdf"
        ],
        "ground_truth": """
The Disaster Recovery SOP describes recovery objectives, failover procedures, communication plans, recovery validation, and business continuity activities.
"""
    },

    {
        "id": 20,
        "query": "What are Kubernetes security best practices?",
        "intent": "best_practices",
        "expected_documents": [
            "BP-001_Kubernetes_Security_Best_Practices.pdf"
        ],
        "ground_truth": """
Best practices include RBAC, Network Policies, Pod Security Standards, Secrets Management, Image Scanning, and regular cluster updates.
"""
    },

    {
        "id": 21,
        "query": "Best practices for CI/CD pipelines.",
        "intent": "best_practices",
        "expected_documents": [
            "BP-002_CICD_Best_Practices.pdf"
        ],
        "ground_truth": """
CI/CD best practices include automated testing, code quality checks, secure secret management, deployment approvals, and rollback automation.
"""
    },

    {
        "id": 22,
        "query": "Logging and monitoring best practices.",
        "intent": "best_practices",
        "expected_documents": [
            "BP-003_Logging_Monitoring_Best_Practices.pdf"
        ],
        "ground_truth": """
Logging and monitoring best practices include centralized logging, structured logs, alerting, observability dashboards, metrics collection, and proactive monitoring.
"""
    }
]