from Neo4j.neo4j_utils import fix_plural_values

plural_query_obj = {
    "Accompanists": "Accompanist",
    "Accountants": "Accountant",
    "Administrators": "Administrator",
    "Advisors": "Advisor",
    "Advocates": "Advocate",
    "Analysts": "Analyst",
    "ANMs": "ANM",
    "Appraisers": "Appraiser",
    "Apprentices": "Apprentice",
    "Architects": "Architect",
    "Artisans": "Artisan",
    "Artists": "Artist",
    "Assistants": "Assistant",
    "Associates": "Associate",
    "Attendants": "Attendant",
    "Attenders": "Attender",
    "Auditors": "Auditor",
    "Bearers": "Bearer",
    "Cashiers": "Cashier",
    "Clerks": "Clerk",
    "Coaches": "Coach",
    "Commandants": "Commandant",
    "Consultants": "Consultant",
    "Coordinators": "Coordinator",
    "Counsellors": "Counsellor",
    "Counselors": "Counselor",
    "Counsels": "Counsel",
    "Curators": "Curator",
    "Demonstrators": "Demonstrator",
    "Developers": "Developer",
    "Doctors": "Doctor",
    "Drivers": "Driver",
    "Editors": "Editor",
    "Educators": "Educator",
    "Engineers": "Engineer",
    "Enumerators": "Enumerator",
    "Executives": "Executive",
    "Experts": "Expert",
    "Facilitators": "Facilitator",
    "Fellows": "Fellow",
    "Fellows": "Fellow",
    "Fellowships": "Fellowship",
    "Friends": "Friend",
    "Graduates": "Graduate",
    "Guards": "Guard",
    "Guides": "Guide",
    "heads": "head",
    "House Keepers": "House Keeper",
    "Inspectors": "Inspector",
    "Instructors": "Instructor",
    "Insulators": "Insulator",
    "Internees": "Internee",
    "Interns": "Intern",
    "Interpretors": "Interpreter",
    "Interviewers": "Interviewer",
    "Investigators": "Investigator",
    "Judges": "Judge",
    "Lascars": "Lascar",
    "LDCs": "LDC",
    "Lecturers": "Lecturer",
    "Librarians": "Librarian",
    "Machinists": "Machinist",
    "Maistries": "Maistry",
    "Malies": "Mali",
    "Managers": "Manager",
    "Massagers": "Massager",
    "Masseurs": "Masseur",
    "Members": "Member",
    "Mentors": "Mentor",
    "Messiers": "Messier",
    "Models": "Model",
    "Nurses": "Nurse",
    "Officers": "Officer",
    "Officers": "Officer",
    "officials": "official",
    "Operators": "Operator",
    "Operators": "Operator",
    "Peons": "Peon",
    "Personnels": "Personnel",
    "Persons": "Person",
    "Pharmacists": "Pharmacist",
    "Physicians": "Physician",
    "Physicians": "Physician",
    "Physicists": "Physicist",
    "Positions": "Position",
    "Practitioners": "Practitioner",
    "Principals": "Principal",
    "Professionals": "Professional",
    "Professors": "Professor",
    "Programmers": "Programmer",
    "Prosecutors": "Prosecutor",
    "Psychologists": "Psychologist",
    "Rangers": "Ranger",
    "Ratings": "Rating",
    "Readers": "Reader",
    "Receptionists": "Receptionist",
    "Recruits": "Recruit",
    "Reporters": "Reporter",
    "Representatives": "Representative",
    "Researchers": "Researcher",
    "Residents": "Resident",
    "Residents": "Resident",
    "RHOs": "RHO",
    "Scholars": "Scholar",
    "Scientists": "Scientist",
    "Screeners": "Screener",
    "Secretaries": "Secretary",
    "Servants": "Servant",
    "Speakers": "Speaker",
    "Specialists": "Specialist",
    "Stenographers": "Stenographer",
    "Stewards": "Steward",
    "Superintendents": "Superintendent",
    "Supervisors": "Supervisor",
    "Surgeons": "Surgeon",
    "Surveyors": "Surveyor",
    "Sweeps": "Sweep",
    "Teachers": "Teacher",
    "Technicians": "Technician",
    "Testers": "Tester",
    "Therapists": "Therapist",
    "Trainees": "Trainee",
    "Tutors": "Tutor",
    "Typists": "Typist",
    "Visitors": "Visitor",
    "Ward Boys": "Ward Boy",
    "Wardens": "Warden",
    "Warders": "Warder",
    "Watchers": "Watcher",
    "Welders": "Welder",
    "Workers": "Worker",
    "Writers": "Writer"
}


fix_plural_values(plural_query_obj)