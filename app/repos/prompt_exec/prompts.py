class Prompts:
    JD_EXTRACTION_PROMPT = """
<Context>
    - Task: Extract ranking criteria from job descriptions for resume scoring
    - Input: Job description text (from PDF/DOCX)
    - Output: List of specific, scoreable criteria
    - Purpose: These criteria will be used to score resumes on a 0-5 scale
</Context>

<Extraction_Requirements>
    <Criteria_Types>
        - Technical Skills: Programming languages, frameworks, tools
        - Experience Requirements: Years of experience, specific domains
        - Educational Qualifications: Degrees, fields of study
        - Certifications: Professional certifications, licenses
        - Domain Knowledge: Industry-specific expertise
        - Soft Skills: Only if explicitly required in JD
    </Criteria_Types>
    
    <Format_Rules>
        - Each criterion must be a single, complete sentence
        - Start with action words: "Must have", "Should have", "X+ years"
        - Include specific measurable requirements where possible
        - Maximum 15 words per criterion
        - Avoid vague terms like "good", "strong" without specifics
    </Format_Rules>
</Extraction_Requirements>

<Output_Guidelines>
    <Structure>
        - Return as a flat list of strings (no categories)
        - Order by importance (most critical first)
        - Each string should be independently scoreable
        - Combine related requirements when possible
    </Structure>
    
    <Quality_Checks>
        - Can this criterion be scored 0-5 against a resume?
        - Is it specific enough to evaluate objectively?
        - Does it avoid company-specific information?
        - Is it a skill/qualification, not a responsibility?
    </Quality_Checks>
</Output_Guidelines>

<Examples>
    <Good_Criteria>
        - "Must have AWS Solutions Architect certification"
        - "5+ years of Python development experience"
        - "Bachelor's degree in Computer Science or related field"
        - "Experience with Docker and Kubernetes"
        - "3+ years of machine learning model deployment"
    </Good_Criteria>
    
    <Poor_Criteria>
        - "Strong communication skills" (too vague)
        - "Work in our Chicago office" (location, not skill)
        - "Passionate about technology" (not measurable)
        - "Join our growing team" (not a criterion)
    </Poor_Criteria>
</Examples>

<Task>
Extract ranking criteria from the following job description:
{{ jd_text }}

Return a JSON list of strings containing only the most important, scoreable criteria for evaluating resumes.
</Task>
    
    """
    RESUME_PROCESSING_PROMPT = """
<Context>
    - Task: Score resume against job criteria
    - Input: Resume text and list of ranking criteria
    - Output: Individual scores (0-5) for each criterion
    - Purpose: Generate scoring data for Excel/CSV export
</Context>

<Scoring_Scale>
    - 0: No evidence of criterion in resume
    - 1: Minimal/tangential evidence 
    - 2: Partial match (below requirement)
    - 3: Meets basic requirement
    - 4: Exceeds requirement
    - 5: Significantly exceeds with strong evidence
</Scoring_Scale>

<Evaluation_Rules>
    - Search for both explicit mentions and implicit evidence
    - Consider synonyms, related terms, and equivalent qualifications
    - For years of experience, calculate from work history dates
    - For certifications, accept only exact matches or higher levels
    - Prioritize recent and relevant experience over older experience
    - Do not infer or assume qualifications not evidenced in resume
</Evaluation_Rules>

<Output_Requirements>
    Return a JSON object with:
    - candidate_name: Extracted from resume
    - scores: Object mapping each criterion to its score (0-5) and brief evidence
    - total_score: Sum of all individual scores
    
    Format:
    {
        "candidate_name": "string",
        "scores": {
            [
            {"criteria_name": "string", "score": number, "evidence": "string"},
            ]
        },
        "score": number
    }
</Output_Requirements>

<Task>
Criteria to evaluate:
{{ criteria }}

Resume to score:
{{ resume }}
</Task>
    """
