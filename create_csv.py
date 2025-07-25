import csv

data = [
    ["subject", "sender", "label"],
    ["Urgent: Payment Overdue", "accounts@company.com", "✅ Important"],
    ["Weekly team meeting notes", "team@company.com", "❌ Not Important"],
    ["Invoice #12345 attached", "billing@vendor.com", "✅ Important"],
    ["Casual Friday Reminder", "hr@company.com", "❌ Not Important"],
    ["Performance Review Discussion", "ceo@company.com", "✅ Important"],
    ["New Event: Tech Conference", "events@newsletter.com", "❌ Not Important"],
    ["Deadline Extended: Project Alpha", "manager@company.com", "✅ Important"],
    ["Company Newsletter - May", "newsletter@company.com", "❌ Not Important"],
    ["Action Required: Approve Budget", "finance@company.com", "✅ Important"],
    ["Lunch & Learn: Calendar Invite", "training@company.com", "❌ Not Important"],
    ["System Downtime Notification", "it-support@company.com", "✅ Important"],
    ["Client Meeting Confirmation", "client@bigcorp.com", "✅ Important"],
    ["Potential Partnership Opportunity", "founder@startuphub.com", "✅ Important"],
    ["Friendly Reminder: Weekly Wellness Tip", "hr@company.com", "❌ Not Important"],
    ["Investment Opportunity: Proposal Attached", "investor@fund.com", "✅ Important"],
    ["New Comment on Your LinkedIn Post", "notifications@linkedin.com", "❌ Not Important"],
    ["Invoice Required: Reimbursement", "admin@company.com", "✅ Important"],
    ["Invitation to Tech Webinar", "marketing@saasplatform.com", "❌ Not Important"],
    ["Reminder: Quarterly OKR Review", "boss@company.com", "✅ Important"],
    ["Business Collaboration Inquiry", "ceo@partnercompany.com", "✅ Important"],
    ["Upcoming Interview Schedule", "hr@company.com", "✅ Important"],
    ["Your Amazon Order Receipt", "no-reply@amazon.com", "❌ Not Important"],
    ["Request for Proposal (RFP)", "procurement@enterprise.com", "✅ Important"],
    ["Event Photos from Last Week", "events@company.com", "❌ Not Important"],
    ["Annual Leave Policy Update", "admin@company.com", "❌ Not Important"],
    ["Final Notice: Action Needed", "support@finance.com", "✅ Important"],
    ["Exclusive Press Release Invitation", "media@publicrelations.com", "✅ Important"],
    ["Team Outing Scheduled", "events@company.com", "❌ Not Important"],
    ["Security Update Required", "security@company.com", "✅ Important"],
    ["Customer Support Ticket Closed", "support@company.com", "❌ Not Important"],
    ["Reminder: Monthly Expense Submission", "accounts@company.com", "✅ Important"],
    ["Meeting Reminder: Project Kickoff", "pm@techcorp.com", "✅ Important"],
    ["Team Social: Friday Happy Hour", "hr@workplace.com", "❌ Not Important"],
    ["Sales Update: Q2 Results", "sales@company.com", "✅ Important"],
    ["Software License Expiring Soon", "licenses@microsoft.com", "✅ Important"],
    ["Newsletter: Weekly Tech Trends", "newsletter@technews.com", "❌ Not Important"],
    ["Invitation to Join Beta Program", "marketing@startup.com", "✅ Important"],
    ["Reminder: Tax Filing Deadline", "tax@government.gov", "✅ Important"],
    ["Special Discount Offer!", "promotions@shopping.com", "❌ Not Important"],
    ["Order Confirmation #78910", "orders@amazon.com", "❌ Not Important"],
    ["Customer Feedback Survey", "noreply@salesforce.com", "❌ Not Important"],
    ["Security Alert: Unusual Activity", "alerts@security.com", "✅ Important"],
    ["Press Release: New Product Launch", "press@innovate.com", "✅ Important"],
    ["Update: Company Holiday Schedule", "admin@company.com", "❌ Not Important"],
    ["Invitation: Annual General Meeting", "investor@bigcorp.com", "✅ Important"],
    ["Weekly Digest", "digest@gmail.com", "❌ Not Important"],
    ["Reminder: Project Timeline Review", "projectlead@techcorp.com", "✅ Important"],
    ["Customer Appreciation Event", "events@luxuryretail.com", "❌ Not Important"],
    ["Urgent: Data Breach Notification", "security@cyberdefense.com", "✅ Important"],
    ["Your Refund Has Been Processed", "refunds@amazon.com", "❌ Not Important"],
    ["Team Building Activity Next Week", "hr@workplace.com", "❌ Not Important"],
    ["Critical System Alert", "it@enterprise.com", "✅ Important"],
    ["Monthly Performance Metrics", "analytics@bigcorp.com", "✅ Important"],
    ["Newsletter: Industry Insights", "newsletter@industrynews.com", "❌ Not Important"],
    ["Project Completion Announcement", "pm@startuphub.com", "✅ Important"],
    ["Internal Memo: New Office Policies", "admin@company.com", "❌ Not Important"],
    ["Press Invitation: Tech Expo 2025", "events@expo.com", "✅ Important"],

    # New data using ❌ Not Important
    ["New Store Opening This Weekend", "info@retailnews.com", "❌ Not Important"],
    ["Don't Miss: Limited-Time Offer", "sales@ecommerce.com", "❌ Not Important"],
    ["Invitation: Art Gallery Launch", "events@artworld.org", "❌ Not Important"],
    ["New Login from Unknown Device", "alerts@cloudsecurity.com", "✅ Important"],
    ["Community Guidelines Update", "notifications@forum.com", "❌ Not Important"],
    ["Congratulations! You Won a Prize", "lottery@scamdomain.net", "❌ Not Important"],
    ["Reminder: Gym Membership Renewal", "support@gymplus.com", "✅ Important"],
    ["Change in Terms of Service", "legal@webapp.com", "✅ Important"],
    ["Weather Alert: Storm Warning", "alerts@weather.gov", "✅ Important"],
    ["Internal Survey: Culture Feedback", "survey@hrtools.com", "❌ Not Important"],
    ["certificate alert:congratulations", "admin@credly.com", "✅ Important"],
    ["certificate alert:congratulations", "admin@udemy.com", "✅ Important"],
  ["Intimation under Section 143(1) of the Income Tax Act", "notifications@incometax.gov.in", "✅ Important"],
  ["e-Campaign – Non-filing of Income Tax Return (ITR)", "e-campaign@incometax.gov.in", "✅ Important"],
  ["Notice under Section 139(9): Defective Return", "notices@incometax.gov.in", "✅ Important"],
  ["High-Value Transaction Alert", "alerts@incometax.gov.in", "✅ Important"],
  ["Update on PAN-Aadhaar Linking Status", "updates@incometax.gov.in", "✅ Important"],
  ["Electricity Bill for May 2025", "billing@tnebnet.org", "✅ Important"],
  ["Water Bill Due Reminder", "noreply@metrowater.tn.gov.in", "✅ Important"],
  ["Credit Card Statement – May 2025", "statements@hdfcbank.com", "✅ Important"],
  ["Loan EMI Due on 25th May", "alerts@icicibank.com", "✅ Important"],
  ["Insurance Policy Renewal Reminder", "services@licindia.in", "✅ Important"],
  ["Admission Confirmation – B.Tech Program", "admissions@annauniv.edu", "✅ Important"],
  ["Upcoming Semester Exam Schedule", "exams@madrasuniversity.ac.in", "✅ Important"],
  ["Certificate Alert: Congratulations!", "admin@udemy.com", "✅ Important"],
  ["Webinar on AI Trends – Register Now", "events@coursera.org", "❌ Not Important"],
  ["New Course Launch: Data Science Basics", "updates@edx.org", "❌ Not Important"],
  ["COVID-19 Vaccination Certificate", "noreply@cowin.gov.in", "✅ Important"],
  ["Aadhaar Update Successful", "uidai@uidai.gov.in", "✅ Important"],
  ["Voter ID Application Status", "election@eci.gov.in", "✅ Important"],
  ["Public Service Announcement: Water Supply Disruption", "info@tn.gov.in", "✅ Important"],
  ["New Guidelines on Waste Management", "environment@tn.gov.in", "❌ Not Important"],
  ["Mega Sale: Up to 70% Off on Electronics!", "deals@flipkart.com", "❌ Not Important"],
  ["Exclusive Offer: Buy 1 Get 1 Free", "promotions@amazon.in", "❌ Not Important"],
  ["Travel Deals: Summer Special Discounts", "offers@makemytrip.com", "❌ Not Important"],
  ["New Arrivals: Fashion Trends 2025", "fashion@limeroad.com", "❌ Not Important"],
  ["Limited-Time Offer: Free Shipping on Orders Above ₹500", "sales@snapdeal.com", "❌ Not Important"],
  ["New Login from Unknown Device", "alerts@cloudsecurity.com", "✅ Important"],
  ["Password Change Confirmation", "security@facebookmail.com", "✅ Important"],
  ["Unusual Activity Detected in Your Account", "noreply@google.com", "✅ Important"],
  ["Two-Factor Authentication Enabled Successfully", "no-reply@twitter.com", "✅ Important"],
  ["Security Alert: Suspicious Login Attempt Blocked", "security@linkedin.com", "✅ Important"]
]



with open("email_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("✅ email_data.csv updated: all 'Not Important' labels now use ❌ symbol.")
