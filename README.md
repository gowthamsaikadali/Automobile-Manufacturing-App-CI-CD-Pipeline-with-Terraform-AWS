# Automobile Manufacturing App
### Flask × AWS × Terraform IaC × GitHub Actions CI/CD

---

## Architecture

```
Internet
   │
   ▼
Application Load Balancer (port 80)
   │
   ▼
EC2 Instance (gunicorn → Flask app, port 5000)
   │
   ▼
RDS MySQL (private subnet, port 3306)
```

**AWS Resources (6 Terraform modules):**

| Module | Resources |
|--------|-----------|
| network | VPC, 2 public subnets, 2 private subnets, IGW, route tables |
| security | ALB SG, EC2 SG, RDS SG |
| iam | EC2 IAM role, instance profile |
| database | RDS MySQL 8.0 (db.t3.micro) |
| alb | ALB, target group, HTTP listener |
| compute | EC2 (Amazon Linux 2), target group attachment |

---

## CI/CD Pipeline  ..

```
Push / PR to main
       │
  ① BUILD     pip install → zip Flask app → upload artifact
       │
  ② TEST      pytest + coverage → publish report in GitHub UI
       │
  ③ TF PLAN   terraform plan → post output as PR comment
       │
  ④ APPROVAL  ⏸ Manual gate — reviewer clicks Approve in GitHub
       │
  ⑤ TF APPLY  terraform apply (uses saved plan)
       │
  ⑥ DEPLOY    SSH → unzip → restart gunicorn → health check
```

---

## One-Time Setup

### 1. Bootstrap remote state (run once locally)
```bash
cd terraform-project/bootstrap
terraform init
terraform apply
```

### 2. GitHub Secrets
`Settings → Secrets and variables → Actions → New repository secret`

| Secret | Value |
|--------|-------|
| `AWS_ACCESS_KEY_ID` | IAM access key |
| `AWS_SECRET_ACCESS_KEY` | IAM secret key |
| `DB_USERNAME` | RDS MySQL username |
| `DB_PASSWORD` | RDS MySQL password |
| `EC2_SSH_PRIVATE_KEY` | Contents of your `.pem` file |
| `FLASK_SECRET_KEY` | Any random 32-char string |
| `RDS_ENDPOINT` | RDS endpoint (after first apply) |

### 3. GitHub Environment (approval gate)
`Settings → Environments → New environment → Name: production → Required reviewers → add yourself`

### 4. Update prod.tfvars
```hcl
key_pair_name = "your-actual-keypair-name"
```

---

## Local Development

```bash
cd app/
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Use SQLite for local dev
export DATABASE_URL=sqlite:///automobile.db
export SECRET_KEY=any-local-secret

python seed.py    # creates admin user
python app.py     # starts Flask dev server
```

Open: http://localhost:5000  
Login: `admin` / `Admin@1234`

---

## Project Structure

```
├── .github/
│   └── workflows/
│       └── cicd.yml               CI/CD pipeline (6 jobs)
├── app/
│   ├── app.py                     Flask app factory
│   ├── extensions.py              db, login_manager
│   ├── models.py                  User, Vehicle, ProductionOrder
│   ├── forms.py                   WTForms
│   ├── health.py                  /health endpoint
│   ├── seed.py                    Admin user bootstrap
│   ├── requirements.txt
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── inventory.py
│   │   └── production.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── inventory/
│   │   └── production/
│   └── tests/
│       └── test_app.py
└── terraform-project/
    ├── bootstrap/                 S3 + DynamoDB for remote state
    ├── environments/
    │   ├── dev/                   Dev environment
    │   └── prod/                  Prod environment ← pipeline target
    └── modules/
        ├── alb/
        ├── compute/
        ├── database/
        ├── iam/
        ├── network/
        └── security/
```
