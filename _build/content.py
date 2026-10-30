"""
VSQC website content — edit copy here, then run:  python _build/build.py
All text comes from "Website Content 2026.docx".
"""

# ---------------------------------------------------------------
# Site settings — CHECK THESE BEFORE LAUNCH
# ---------------------------------------------------------------
SITE = {
    "name": "VSQC",
    "legal": "Vaishno Sai Quality Consultants Pvt. Ltd.",
    # Where contact / RFQ / feedback / grievance mail goes (mailto fallback)
    "email": "info@vsqc.in",
    # Optional form backend (e.g. Formspree, Google Apps Script). When set, forms POST
    # here instead of opening the visitor's email app. Required for anonymous reports.
    "form_endpoint": "",
    # Portal sign-in addresses
    "portal_customer_url": "",
    "portal_employee_url": "",
    "offices": ["India", "Sri Lanka", "UAE"],
}

# ---------------------------------------------------------------
# Services — order = order of the home-page scroll showcase.
# `loop` = the looping clip for that service (clip-3, clip-5 …)
# ---------------------------------------------------------------
SERVICES = [
    {
        "slug": "iso",
        "short": "ISO & Audits",
        "title": "Management System & ISO Consultancy & Audits",
        "line": "From gap assessment to certification, across 35+ standards.",
        "intro": "Achieve global standards of excellence with our expert ISO implementation and auditing services. We guide you through seamless certification journeys tailored to your operational scope.",
        "tags": "Gap assessment · Documentation · Internal audits · Certification support",
        "loop": 3,
        "items": [
            ("Gap Assessment", "Evaluating the current state of your systems against desired standards. We identify critical operational gaps and establish a clear roadmap for successful implementation."),
            ("Implementation Roadmap", "A structured, step-by-step strategic plan guiding your organization toward compliance. We outline timelines, responsibilities, and key milestones to ensure efficient execution."),
            ("Documentation Development", "Creating customized, compliant documentation tailored to your organizational processes. This includes manuals, procedures, and standard operating protocols required for certification."),
            ("Implementation Assistance", "Hands-on support integrating new management frameworks into your daily operations. Our consultants work alongside your team to ensure practical and sustainable adoption."),
            ("Training (Awareness, Lead Implementers, Internal Auditor)", "Comprehensive educational modules designed to build internal competency at all levels. We equip your staff with the knowledge needed to maintain and audit your management systems."),
            ("Internal Audits and Reviews", "Rigorous pre-certification evaluations conducted by our experts to verify system effectiveness. We help identify non-conformities and implement corrective actions before external audits."),
            ("External Audit & Certification Support", "Dedicated assistance during your official third-party certification audits. We liaise with certification bodies and support your team in demonstrating compliance."),
            ("Post Certification Support (AMC)", "Ongoing Annual Maintenance Contracts to ensure your systems remain compliant and continually improve. We provide regular reviews and updates to adapt to changing standards."),
            ("Digital Transformation Link for Management Systems", "Seamlessly integrate your management systems with our proprietary digital tools. Automate workflows and track compliance metrics in real-time."),
        ],
        "standards": True,
    },
    {
        "slug": "esg",
        "short": "ESG & Sustainability",
        "title": "ESG / Sustainability Implementation Consultancy & Assurance Assessments",
        "line": "Build your ESG roadmap, measure impact and report with confidence.",
        "intro": "Drive sustainable growth and meet global ESG mandates with our specialized sustainability frameworks. We help you measure, manage, and report your environmental and social impact effectively.",
        "tags": "Materiality · Carbon, water & energy · ESG reporting · EcoVadis & SEDEX ratings",
        "loop": 5,
        "items": [
            ("ESG Gap Assessment", "Evaluating your current ESG maturity against global standards. We identify critical sustainability gaps and outline steps for improvement."),
            ("Materiality Assessment", "Identifying and prioritizing the ESG issues that matter most to your business and stakeholders. This forms the foundation of a robust sustainability strategy."),
            ("ESG Roadmap Development", "Crafting a strategic timeline to achieve your short- and long-term sustainability goals. We align your roadmap with global frameworks and business objectives."),
            ("Policies and Procedures Development", "Drafting comprehensive ESG guidelines tailored to your operational reality. We ensure your policies reflect industry best practices and regulatory requirements."),
            ("Environmental Initiatives Support", "Providing expert guidance to execute practical environmental conservation and efficiency projects. We help turn your sustainability goals into measurable actions."),
            ("Carbon, Water & Energy Assessment and Management", "Quantifying your resource footprint to establish baseline metrics. We design management strategies to optimize usage, reduce costs, and lower emissions."),
            ("Life Cycle Assessments", "Analyzing the environmental impacts of your products from raw material extraction to end-of-life disposal. Helps in designing eco-friendly products and improving processes."),
            ("Human Rights Implementation", "Integrating fair labor practices and human rights protections into your corporate framework. Ensures ethical treatment of workers across your supply chain."),
            ("Antibribery and Fair Trade Practices Implementation", "Establishing strict ethical guidelines to prevent corruption and ensure fair business dealings. Builds trust and compliance with international anti-bribery laws."),
            ("Information Security and Data Privacy Implementation", "Aligning your ESG goals with robust data protection and privacy standards. Ensures your corporate governance covers critical digital risks."),
            ("Business Resilience Implementation", "Building operational fortitude to withstand and quickly recover from environmental and economic shocks. Ensures long-term sustainability of the business model."),
            ("Product Stewardship Implementation", "Managing the health, safety, and environmental impacts of different products throughout their lifecycle. Promotes responsible product development and disposal."),
            ("Training (Awareness, Internal Auditors)", "Educating your team on ESG principles and training internal auditors to monitor sustainability performance. Builds a culture of corporate responsibility."),
            ("Supplier ESG Audits", "Evaluating your supply chain vendors for adherence to environmental and social governance standards. Mitigates third-party risks and ensures ethical sourcing."),
            ("ESG Reporting", "Compiling detailed, transparent sustainability reports aligned with frameworks like GRI or SASB. Communicates your ESG achievements clearly to stakeholders."),
            ("ESG Ratings Support — EcoVadis, GEE ESG, SEDEX", "Guiding your organization through complex ESG rating platforms to maximize your scores. We streamline data collection and evidence submission for platforms like EcoVadis."),
            ("Digital Transformation Links (GEE Portal)", "Leverage the GEE Portal for automated ESG ratings, supplier audits, and human rights assessments. A centralized digital hub for all your sustainability metrics."),
        ],
    },
    {
        "slug": "vendor",
        "short": "Vendor Development",
        "title": "Vendor Development & Audits",
        "line": "Select, train, monitor and rate the vendors you depend on.",
        "intro": "Strengthen your supply chain with our comprehensive vendor evaluation and capacity-building programs. Ensure your partners align with your quality, EHS, and sustainability standards.",
        "tags": "Selection audits · Capacity building · Cluster development · Vendor ratings",
        "loop": 7,
        "items": [
            ("Vendor Selection Audits", "Comprehensive evaluations of potential vendors covering Quality, EHS, Sustainability, Social, and InfoSec criteria. Ensures you partner with compliant and reliable suppliers."),
            ("Vendor Training and Capacity Building", "Upskilling your supply chain partners to meet your specific operational standards. We provide targeted training to improve vendor performance and compliance."),
            ("Cluster Development", "Strategic grouping and development of vendors to foster collaborative improvement and economies of scale. Enhances the overall resilience of your supply network."),
            ("Vendor Monitoring", "Continuous oversight of supplier performance using data-driven metrics. We help identify potential supply chain risks before they impact your operations."),
            ("Vendor Compliance Audits", "Periodic, rigorous audits to verify that existing vendors continue to meet all contractual and regulatory obligations. Ensures sustained supply chain integrity."),
            ("Vendor Ratings", "Implementing structured scoring systems to objectively evaluate and rank suppliers based on performance. Helps in making informed procurement decisions."),
        ],
    },
    {
        "slug": "training",
        "short": "Training & Mentorship",
        "title": "Training & Mentorship",
        "line": "Classroom and online training, from awareness to lead auditor.",
        "intro": "Empower your workforce with targeted awareness and lead auditor training programs. Our expert mentors deliver customized modules to bridge competency gaps and foster continuous improvement.",
        "tags": "Needs identification · Internal auditor · Lead implementer · Lead auditor with CBs",
        "loop": 9,
        "items": [
            ("Customised Classroom and Online Trainings", "Flexible, blended learning solutions tailored to your specific organizational needs. We deliver engaging content both in-person and via digital platforms."),
            ("Training Module Development", "Designing bespoke curriculum and course materials focused on your operational standards. Content is developed by industry experts for maximum impact."),
            ("LMS Management", "End-to-end administration of your Learning Management System. We help track employee progress, manage course catalogs, and ensure seamless delivery."),
            ("Training Needs Identification", "Analyzing workforce competencies to pinpoint knowledge gaps. We develop strategic training plans to elevate your team's overall skill level."),
            ("Awareness Courses for all ISO / IATF, AS, SA Standards", "Foundational training designed to introduce staff to core concepts of various management standards. Essential for building a compliance-focused organizational culture."),
            ("Lead Implementers Training", "Advanced, in-depth programs equipping key personnel with the skills to drive system implementation. Prepares your leaders to manage complex compliance projects."),
            ("Internal Auditor Training", "Teaching your staff how to conduct effective internal assessments and identify non-conformances. Critical for maintaining continuous improvement and audit readiness."),
            ("Lead Auditor Training Jointly with CBs", "Elite certification programs conducted in partnership with leading Certification Bodies. Qualifies your professionals to lead third-party compliance audits."),
        ],
    },
    {
        "slug": "digital",
        "short": "Digital Transformation",
        "title": "Digital Transformation for Management Systems",
        "line": "Move your management systems onto AI-supported digital tools.",
        "intro": "Modernize your compliance and operational frameworks with AI-driven digital tools. Streamline audits, document management, and risk assessments through our innovative software solutions.",
        "tags": "Online audit tools · Document control · AI-based MIS & KPIs · Risk & BIA tools",
        "loop": 11,
        "items": [
            ("Digitisation of Management Systems with AI", "Upgrading traditional, manual processes into smart, automated workflows using Artificial Intelligence. Enhances accuracy, speed, and predictive capabilities."),
            ("Online Audit Tools", "Streamline the entire auditing process with cloud-based software. Facilitates remote assessments, instant reporting, and real-time collaboration."),
            ("Document Management Tools", "Securely store, organize, and control access to critical compliance documentation. Ensures version control and immediate retrieval during audits."),
            ("MIS and KPI Tools with AI Based Analysis", "Advanced Management Information Systems that track performance indicators automatically. AI-driven insights help leadership make informed, data-backed decisions."),
            ("Risk Management Tools", "Digital platforms for identifying, evaluating, and mitigating organizational risks in real-time. Provides dynamic dashboards for proactive risk governance."),
            ("BIA Tools", "Business Impact Analysis software to quantify the effects of potential operational disruptions. Essential for robust business continuity planning."),
            ("Project Management Tools", "Integrated software to plan, execute, and monitor compliance and implementation projects. Keeps teams aligned on tasks, timelines, and resources."),
            ("Communication Planners", "Digital scheduling and communication platforms ensuring transparent information flow across the organization. Keeps stakeholders informed on management system updates."),
        ],
    },
    {
        "slug": "infosec",
        "short": "Information Security",
        "title": "Information Security, Data Privacy & Cybersecurity",
        "line": "Implement and audit the controls that protect your data.",
        "intro": "Protect your critical assets and ensure compliance with stringent data privacy regulations. We offer robust cybersecurity assessments, VAPT, and information security management systems.",
        "tags": "IT security audits · VAPT · DPIA · RoPA · Incident management",
        "loop": 13,
        "items": [
            ("Infosec Controls Monitoring and Statement of Applicability", "Continuous tracking of security controls to ensure they remain effective and relevant. We help you maintain an accurate, up-to-date Statement of Applicability (SoA)."),
            ("IT Security Audits", "In-depth reviews of your IT infrastructure to identify vulnerabilities and verify compliance with security policies. Ensures your network is resilient against threats."),
            ("VAPT — Vulnerability Assessment and Penetration Testing", "Proactive simulated cyberattacks and scans utilizing advanced online tools to expose system weaknesses. Helps patch vulnerabilities before malicious exploitation."),
            ("DPIA — Data Privacy Impact Assessment", "Systematic evaluations to identify and minimize the data protection risks of a project. Ensures your processes comply with global privacy laws like GDPR."),
            ("RoPA Asset Management", "Establishing and maintaining a comprehensive Record of Processing Activities. Keeps track of all personal data flow within your organization."),
            ("Configuration Management", "Ensuring all IT systems and software are configured securely according to industry best practices. Reduces the attack surface of your network."),
            ("Ticket and Incident Management", "Structured systems for recording, tracking, and resolving security events efficiently. Ensures swift response to minimize impact during a security breach."),
        ],
    },
    {
        "slug": "safety",
        "short": "Health & Safety",
        "title": "Health & Safety Implementation & Audits",
        "line": "Audits, inspections and risk studies that keep people safe.",
        "intro": "Foster a secure working environment with our comprehensive health and safety audits. We provide strategic safety metrics tracking and hazard mitigation frameworks to protect your workforce.",
        "tags": "Safety audits · Incident investigation · HIRA · HAZOP · JSA · LOPA",
        "loop": 15,
        "items": [
            ("EHS Project Management", "End-to-end planning and execution of Environmental, Health, and Safety initiatives. We ensure your safety projects are delivered on time and within compliance mandates."),
            ("Safety Audits and Inspections", "Thorough on-site evaluations to identify workplace hazards and assess compliance with safety regulations. We provide actionable recommendations for risk mitigation."),
            ("Safety Training and Testing", "Equipping your workforce with essential safety knowledge and conducting practical drills. Ensures employees are prepared to handle workplace emergencies."),
            ("Incident Investigation", "Root-cause analysis of workplace accidents or near-misses. We help implement preventive measures to ensure incidents are not repeated."),
            ("Safety Performance Tracking", "Monitoring leading and lagging safety indicators using specialized metrics. Provides visibility into the effectiveness of your EHS programs."),
            ("HIRA, HAZOP, JSA, LOPA", "Advanced risk assessment methodologies including Hazard Identification, Operability Studies, and Job Safety Analysis. Comprehensive tools to isolate and control high-level operational risks."),
        ],
    },
]

# ---------------------------------------------------------------
# Logo carousel — clients & certification partners (from the content doc).
# (display name, file slug, small tag, wordmark style)
# To use the official logo, put  logos/<slug>.svg  (or .png) next to index.html
# and rebuild — the carousel switches from the typeset wordmark to the file.
# ---------------------------------------------------------------
LOGOS = [
    ("TÜV Rheinland", "tuv-rheinland", "Certification partner", "sans"),
    ("Tata Realty", "tata-realty", "Client", "serif"),
    ("BSI", "bsi", "Certification partner", "caps"),
    ("Gemsons Precision", "gemsons-precision", "Client", "serif"),
    ("LRQA", "lrqa", "Certification partner", "caps"),
]

# ---------------------------------------------------------------
# Standards (ISO page) — code, name, description
# ---------------------------------------------------------------
STANDARDS = [
    ("ISO 9001", "Quality Management System", "The globally recognized standard for quality management, applicable to all organizations. Enhances customer satisfaction and drives continuous process improvement."),
    ("ISO 13485", "Medical Device Management", "Ensures consistent design, development, and production of safe medical devices. Critical for meeting strict regulatory requirements in the healthcare sector."),
    ("ISO 14001", "Environment Management Systems", "A framework for managing environmental responsibilities in a systematic manner. Helps organizations reduce waste, improve resource efficiency, and meet environmental regulations."),
    ("ISO 14064", "Greenhouse Gas (GHG)", "Provides a standardized approach for quantifying and reporting greenhouse gas emissions. Essential for organizations aiming to track and reduce their carbon footprint."),
    ("ISO 17025", "Laboratory Management Systems", "The main standard for testing and calibration laboratories ensuring reliable results. Validates technical competence and promotes confidence in laboratory operations."),
    ("ISO 19443", "Nuclear Quality Management System", "Applies quality management principles specifically to the nuclear energy supply chain. Focuses on nuclear safety culture and critical compliance requirements."),
    ("ISO 20000-1", "IT Service Management System", "Defines requirements for establishing, implementing, and maintaining effective IT service management. Ensures IT services are aligned with business needs and global best practices."),
    ("ISO 20121", "Event Sustainability Management Systems", "Provides a framework to improve the sustainability of events throughout their entire cycle. Helps organizers manage social, economic, and environmental impacts."),
    ("ISO 21001", "Education Organisation Management System", "A management system standard tailored specifically for educational institutions. Focuses on enhancing the learning environment and meeting the needs of learners and staff."),
    ("ISO 22000", "Food Safety Management Systems", "Integrates quality management with food safety to prevent hazards across the food chain. Ensures safe consumption from farm to fork."),
    ("ISO 22163", "Railways Management Systems", "Sets stringent quality requirements for the rail industry supply chain. Enhances product quality, safety, and reliability in railway sector manufacturing."),
    ("ISO 22301", "Business Continuity Management Systems", "Prepares organizations to respond to and recover from unexpected disruptive incidents. Ensures operational resilience and safeguards organizational reputation."),
    ("ISO 26000", "Social Responsibility", "Provides guidance on how businesses can operate in a socially responsible way. Helps organizations translate CSR principles into effective actions."),
    ("ISO 27001", "Information Security Management Systems", "A systematic approach to managing sensitive company information so that it remains secure. Protects data confidentiality, integrity, and availability against cyber threats."),
    ("ISO 27017", "Information Security for Cloud Service Providers", "Provides specialized information security controls tailored for the provision and use of cloud services. Enhances trust and security in cloud computing environments."),
    ("ISO 27018", "Data Privacy for Cloud Providers", "Establishes commonly accepted control objectives to protect Personally Identifiable Information (PII) in public clouds. Ensures cloud privacy compliance."),
    ("ISO 27701", "Privacy Information Management Systems", "An extension to ISO 27001 focusing specifically on privacy management and PII protection. Helps organizations comply with global privacy regulations like GDPR."),
    ("ISO 28000", "Logistics Security Management Systems", "Specifies the requirements for a security management system within the supply chain. Protects logistics operations from theft, terrorism, and other security threats."),
    ("ISO 29001", "Petroleum Quality Management Systems", "Defines quality management system requirements for product and service supply organizations for the petroleum, petrochemical, and natural gas industries."),
    ("ISO 30414", "Human Resource Management Systems", "Provides guidelines for internal and external human capital reporting. Helps organizations measure and highlight the contribution of their workforce."),
    ("ISO 31000", "Risk Management Systems", "Provides principles and generic guidelines on managing risks faced by organizations. Helps in decision-making and protecting organizational assets."),
    ("ISO 37001", "Antibribery Management Systems", "Specifies requirements for establishing systems to prevent, detect, and address bribery. Promotes ethical business cultures and legal compliance."),
    ("ISO 37301", "Compliance Management Systems", "Provides guidelines for establishing, developing, and maintaining an effective compliance management system. Ensures organizations adhere to relevant laws and regulations."),
    ("ISO 39001", "Road Traffic Safety Management Systems", "Sets out requirements for organizations interacting with the road traffic system to reduce death and serious injuries. Promotes proactive road safety practices."),
    ("ISO 41001", "Facility Management Systems", "Standardizes facility management practices to improve organizational efficiency and workspace quality. Integrates people, place, and process within the built environment."),
    ("ISO 45001", "Occupational Health & Safety Management Systems", "The premier standard for occupational health and safety, aimed at reducing workplace injuries and illnesses. Promotes a proactive culture of health and safety."),
    ("ISO 50001", "Energy Management Systems", "Provides a practical way to improve energy use through the development of an energy management system. Helps reduce energy costs and greenhouse gas emissions."),
    ("ISO 55001", "Asset Management Systems", "Specifies requirements for the effective management of physical and intangible assets. Maximizes value realization from assets across their lifecycle."),
    ("AS 9100", "Aerospace Management Systems", "The internationally recognized Quality Management System standard specific to the aerospace, aviation, and defense industries. Ensures safety, reliability, and regulatory compliance."),
    ("IATF 16949", "Automotive Quality Management Systems", "The global technical specification and quality management standard for the automotive industry. Focuses on continuous improvement, defect prevention, and waste reduction."),
    ("TL 9000", "Telecommunication Management System", "A quality management system designed specifically for the telecommunications industry. Focuses on supply chain directives, performance metrics, and service reliability."),
    ("SA 8000", "Social Accountability Management Systems", "An auditable certification standard that encourages organizations to develop, maintain, and apply socially acceptable practices in the workplace."),
    ("RJC", "Responsible Jewellery Council", "Sets standards for responsible business practices across the jewelry supply chain. Covers ethical, human rights, social, and environmental considerations."),
    ("BEC 1500", "Human Rights Management", "A framework dedicated to ensuring the protection and promotion of human rights within corporate operations and supply chains."),
    ("BEC 100", "Housekeeping Management Systems", "Standardizes facility housekeeping processes to ensure hygiene, safety, and operational efficiency in managed environments."),
    ("NABH", "Accreditation for Hospitals", "A national healthcare accreditation standard ensuring high-quality patient care and safety. Focuses on continuous quality improvement in hospital administration."),
    ("BPR", "Business Process Restructuring", "Analyzing and redesigning core business workflows to achieve dramatic improvements in productivity and quality. Optimizes operations for maximum efficiency."),
]

# ---------------------------------------------------------------
# Home page copy
# ---------------------------------------------------------------
HOME = {
    "welcome": "Welcome to VSQC, your comprehensive partner for Management Systems, ESG, and Digital Transformation. We offer end-to-end consulting, auditing, and training services tailored to drive your organization's excellence and compliance.",
    "services_intro": "Explore our diverse range of specialized services designed to elevate your business operations. From ISO consultancy, sustainability to cybersecurity, find the right solutions for your specific industry needs.",
    "index": [
        ("portal.html", "VSQC Portal", "Access your personalized dashboard to track project progress, audit reports, and compliance metrics. A secure, unified gateway for our clients and team members."),
        ("achievements.html", "Our Achievements", "Discover our track record of successful multi-site certifications and industry breakthroughs. Read how we have transformed businesses through dedication and specialized expertise."),
        ("policies.html", "Our Policies", "Review our foundational commitments to quality, sustainability, and ethical business practices. Our transparent policies reflect our dedication to integrity and continuous improvement."),
        ("team.html", "Our Team & Partners", "Meet the experienced professionals and strategic partners who drive VSQC's success. Our multi-disciplinary team brings decades of industry experience to every engagement."),
        ("contact.html", "Contact Us", "Connect with our global offices in India, Sri Lanka, and the UAE for tailored consultancy solutions. Reach out for RFQs, feedback, or to start your compliance journey today."),
    ],
}

# ---------------------------------------------------------------
# Other pages
# ---------------------------------------------------------------
ACHIEVEMENTS = {
    "intro": "Discover our track record of successful multi-site certifications and industry breakthroughs. Read how we have transformed businesses through dedication and specialized expertise.",
    "rows": [
        ("Case Studies & Multisite Certifications", "Detailed insights into our successful projects, including complex multi-site, multi-standard certifications. See how we drive compliance at scale."),
        ("Client Testimonials", "Hear directly from industry leaders like Tata Realty and Gemsons Precision about their experience with VSQC. Proven success from satisfied partners."),
        ("Our Certifications and Accreditation", "We are a trusted Consulting Partner with top-tier certification bodies like TUV-R, BSI, and LRQA. We hold our own ISO 9001:2026 and ISO 27001:2022 certifications."),
    ],
    "clients": ["Tata Realty", "Gemsons Precision"],
    "partners": ["TUV-R", "BSI", "LRQA"],
    "own_certs": [("ISO 9001:2026", "Quality Management System"), ("ISO 27001:2022", "Information Security Management System")],
}

POLICIES = {
    "intro": "Review our foundational commitments to quality, sustainability, and ethical business practices. Our transparent policies reflect our dedication to integrity and continuous improvement.",
    "policies": [
        ("ESG Policy", "Our commitment to environmental, social and governance responsibility across every engagement."),
        ("Whistleblower Policy", "Secure, confidential channels for reporting concerns, with protection for those who speak up."),
        ("Quality Policy", "Our commitment to consistent, high-quality consulting, auditing and training outcomes."),
    ],
    "policies_note": "Access our publicly available commitments to quality, ethical conduct, and sustainability. Transparent governance documents that define our corporate integrity.",
    "processes": [
        ("Consulting", "Clear, standardized methodologies detailing how we deliver our consultancy services, from gap assessment through certification and beyond."),
        ("Training", "How we identify needs, design modules and deliver classroom and online training, including lead auditor programs with certification bodies."),
        ("Onsite Manpower", "How we deploy experienced professionals onsite to support your management systems day to day."),
    ],
    "processes_note": "Clear, standardized methodologies detailing how we deliver our consultancy and training services. Ensures consistency and high-quality results for every client engagement.",
}

TEAM = {
    "intro": "Meet the experienced professionals and strategic partners who drive VSQC's success. Our multi-disciplinary team brings decades of industry experience to every engagement.",
    # Add people here as ("Name", "Role", "photo-file.jpg or ''"). Section hides while empty.
    "people": [],
}

CONTACT = {
    "intro": "Connect with our global offices in India, Sri Lanka, and the UAE for tailored consultancy solutions. Reach out for RFQs, feedback, or to start your compliance journey today.",
}

PORTAL = {
    "intro": "Access your personalized dashboard to track project progress, audit reports, and compliance metrics. A secure, unified gateway for our clients and team members.",
}
