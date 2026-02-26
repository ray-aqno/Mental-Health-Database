# College Mental Health Resources Data Collection Template

Use this template to gather information about mental health resources at colleges in your region.

## Instructions

1. For each college, fill out one section
2. Get coordinates from Google Maps (search "University Name" ? right-click ? coordinates)
3. Find mental health office websites for detailed information
4. Include ALL mental health-related services (counseling, psychiatry, crisis, peer support, etc.)
5. Provide freshman-specific information (how to schedule, walk-in availability, etc.)

---

## COLLEGE 1

### College Information
- **College Name**: ___________________________
- **Location (City, State)**: ___________________________
- **Website**: ___________________________
- **Latitude**: ___________________________
- **Longitude**: ___________________________

### Mental Health Resource 1
- **Service Name**: ___________________________
- **Description**: ___________________________
- **Contact Email**: ___________________________
- **Contact Phone**: ___________________________
- **Service Website**: ___________________________
- **Department**: ___________________________
- **Office Hours**: ___________________________
- **Physical Location**: ___________________________
- **Freshman Notes**: ___________________________

### Mental Health Resource 2
- **Service Name**: ___________________________
- **Description**: ___________________________
- **Contact Email**: ___________________________
- **Contact Phone**: ___________________________
- **Service Website**: ___________________________
- **Department**: ___________________________
- **Office Hours**: ___________________________
- **Physical Location**: ___________________________
- **Freshman Notes**: ___________________________

### Mental Health Resource 3
- **Service Name**: ___________________________
- **Description**: ___________________________
- **Contact Email**: ___________________________
- **Contact Phone**: ___________________________
- **Service Website**: ___________________________
- **Department**: ___________________________
- **Office Hours**: ___________________________
- **Physical Location**: ___________________________
- **Freshman Notes**: ___________________________

---

## COLLEGE 2

### College Information
- **College Name**: ___________________________
- **Location (City, State)**: ___________________________
- **Website**: ___________________________
- **Latitude**: ___________________________
- **Longitude**: ___________________________

### Mental Health Resource 1
- **Service Name**: ___________________________
- **Description**: ___________________________
- **Contact Email**: ___________________________
- **Contact Phone**: ___________________________
- **Service Website**: ___________________________
- **Department**: ___________________________
- **Office Hours**: ___________________________
- **Physical Location**: ___________________________
- **Freshman Notes**: ___________________________

### Mental Health Resource 2
- **Service Name**: ___________________________
- **Description**: ___________________________
- **Contact Email**: ___________________________
- **Contact Phone**: ___________________________
- **Service Website**: ___________________________
- **Department**: ___________________________
- **Office Hours**: ___________________________
- **Physical Location**: ___________________________
- **Freshman Notes**: ___________________________

### Mental Health Resource 3
- **Service Name**: ___________________________
- **Description**: ___________________________
- **Contact Email**: ___________________________
- **Contact Phone**: ___________________________
- **Service Website**: ___________________________
- **Department**: ___________________________
- **Office Hours**: ___________________________
- **Physical Location**: ___________________________
- **Freshman Notes**: ___________________________

---

## [Repeat for additional colleges...]

---

## Tips for Data Collection

### Finding Coordinates
1. Go to Google Maps
2. Search for college name
3. Right-click on the main campus location
4. Copy latitude and longitude

Example: `40.1164, -88.2434`

### Finding Mental Health Resources
1. Visit college website
2. Look for: "Student Health", "Counseling", "Mental Health", "Wellness"
3. Common locations:
   - Student Health/Medical Services
   - Dean of Students Office
   - Student Wellness Center
   - Psychology Department

### Freshman Information
Include:
- How to make first appointment
- Walk-in hours available?
- Any special freshman orientation/intake process
- What to bring (insurance card, ID, etc.)
- Wait times typically expected
- Whether parents can call on behalf of student

### Service Types to Include
- [ ] Counseling Center
- [ ] Psychiatric Services
- [ ] Crisis/Emergency Services
- [ ] Peer Support Groups
- [ ] Substance Abuse Services
- [ ] Eating Disorder Services
- [ ] LGBTQ+ Support
- [ ] Disability Services (mental health)
- [ ] Wellness Center
- [ ] 24/7 Hotline

### Contact Information Format
- **Email**: Use full institutional email (not personal)
- **Phone**: Include full number with country code: +1-XXX-XXX-XXXX
- **Website**: Full URL including https://
- **Hours**: Use 12-hour format (8AM-5PM, not 08:00-17:00)

---

## Sample Data Entry

### College Example
- **College Name**: University of Illinois Urbana-Champaign
- **Location**: Urbana, Illinois
- **Website**: https://www.illinois.edu
- **Latitude**: 40.1164
- **Longitude**: -88.2434

### Resource Example
- **Service Name**: Counseling Center
- **Description**: Free, confidential individual and group counseling for all students
- **Contact Email**: counseling@illinois.edu
- **Contact Phone**: +1-217-333-3704
- **Service Website**: https://www.counselingcenter.illinois.edu
- **Department**: Student Affairs
- **Office Hours**: Monday-Friday, 8AM-5PM
- **Physical Location**: Student Wellness Center, Room 101
- **Freshman Notes**: New students can schedule orientation appointments online at mycounseling.illinois.edu or call for same-day emergency appointments

---

## Verification Checklist

Before submitting data:
- [ ] All colleges have valid coordinates
- [ ] All emails are institutional addresses
- [ ] All phone numbers include country code
- [ ] All URLs start with https://
- [ ] Office hours are clearly formatted
- [ ] Each college has at least 1 resource
- [ ] Freshman notes are specific and helpful
- [ ] No spaces in phone numbers or extra characters in emails
- [ ] Department names are consistent with college structure
- [ ] All required fields are filled (no blanks)

---

## Next Steps

1. Complete this form for all target colleges
2. Save as a filled-in text document or spreadsheet
3. Convert to the JSON format shown in `sample_colleges_data.json`
4. Run the data importer: `python Scripts/data_importer.py`
5. Verify colleges appear on the map

---

## Contact Information Format Examples

### Phone Numbers
- ? Correct: `+1-217-333-3704`
- ? Wrong: `217-333-3704`
- ? Wrong: `(217) 333-3704`

### Emails
- ? Correct: `counseling@illinois.edu`
- ? Wrong: `john.smith@gmail.com`
- ? Wrong: `counseling @ illinois.edu`

### Websites
- ? Correct: `https://www.counselingcenter.illinois.edu`
- ? Wrong: `www.counselingcenter.illinois.edu`
- ? Wrong: `http://counselingcenter.illinois.edu`

### Hours
- ? Correct: `Monday-Friday, 8AM-5PM`
- ? Correct: `Monday-Thursday, 9AM-6PM; Friday, 9AM-4PM`
- ? Wrong: `8-5 M-F`
- ? Wrong: `08:00-17:00`

---

## Questions to Ask College

When contacting colleges for updated information:

1. "What mental health services does your campus offer?"
2. "How do freshmen typically access these services?"
3. "Are there walk-in hours or only scheduled appointments?"
4. "What should a student bring to their first appointment?"
5. "Do services cost anything for enrolled students?"
6. "Are there any special resources for freshmen?"
7. "What crisis resources are available 24/7?"
8. "Are there online or telehealth options?"
9. "What is the typical wait time for an appointment?"
10. "Are parent/guardian calls accepted?"

---

Save your completed data and let me know when you're ready to import!
