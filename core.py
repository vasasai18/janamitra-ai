"""Source-bounded pension information for the Janamitra AI demo.
This is a DEMO knowledge base, not an eligibility determination service.
"""
from __future__ import annotations
import re

SOURCES = {
    "scheme": "https://sspensions.ap.gov.in/SSP",
    "eligibility": "https://sspensions.ap.gov.in/SSP/Home/About",
    "order": "https://sspensions.ap.gov.in/SSP/Documents/GO%20MS%2043%2013.06.2024.pdf",
}

# Verified from the official Andhra Pradesh government sources listed above.
# CAUTION: the About page still displays pre-2024 amounts; never use its old Rs 2,250.
FACTS = """NTR Bharosa Pension Scheme is an Andhra Pradesh government social-security pension programme.
Old-age pension: The About/eligibility page lists 60 years and above and describes a person as destitute (little or no means of subsistence and no family or relative to depend upon).
The eligibility page also lists common criteria: BPL family with white ration card; local resident of the district; not covered by another pension scheme. These are the published website criteria and may need checking against later government orders.
Government Order G.O.Ms.No.43 dated 13 June 2024 increased the old-age pension amount to Rs 4,000 per month, payable from July 2024. An older About page still shows a previous Rs 2,250 amount; do not report that as the current rate.
In rural areas, the MPDO is listed as sanctioning authority; in urban areas, the Municipal Commissioner.
Information about whether new applications are currently open, every document currently required, and an individual's final eligibility has NOT been verified for this demo. Advise users to check with their local Grama/Ward Sachivalayam or official authorities.
""".strip()

ENGLISH = {
    "age": "The government's pension eligibility page lists **60 years or above** for the old-age pension category. Age alone does not prove eligibility; other published criteria must also be checked.",
    "amount": "The AP Government's **G.O.Ms.No.43 (13 June 2024)** increased the old-age pension to **₹4,000 per month**, payable from July 2024. The older About page shows a previous amount; the later government order is the source for ₹4,000.",
    "eligibility": "For AP old-age pension, the published About page lists **60+ years**, destitution, **BPL/white ration card**, district residence and not being covered by another pension scheme. These are guidance points, **not an approval decision**. Verify the latest conditions with the official authority.",
    "apply": "I cannot verify that new pension applications are **currently open**. Please confirm the active application process and any deadline with your **Grama/Ward Sachivalayam** or the official pension website. Do not share your Aadhaar number or account details here.",
    "documents": "I have not verified a complete, up-to-date document checklist. Please check the official instructions or ask your local Grama/Ward Sachivalayam for the current list before applying. Avoid sharing personal ID numbers in this demo.",
    "general": "I can explain Andhra Pradesh's **NTR Bharosa old-age pension** using official sources. Try asking about **minimum age, pension amount, published eligibility, documents or application process**. If the official sources do not cover your question, I won't guess.",
}
TELUGU = {
    "age": "AP old-age pension ki official eligibility page prakaram **60 samvatsaralu leda antakante ekkuva** vayasu undali. Vayasu okkate saripodu; migatha conditions kuda verify cheyyali.",
    "amount": "AP Government **G.O.Ms.No.43 (13 June 2024)** prakaram old-age pension **₹4,000 per month**, July 2024 nunchi applicable. Older About page lo previous amount undi; newer GO ni follow cheyyali.",
    "eligibility": "Official About page prakaram old-age pension ki **60+ age**, destitute condition, **BPL/white ration card**, district residence, vere pension scheme coverage lekapovadam lanti conditions unnayi. Ivi preliminary information matrame—**final eligibility approval kaadu**. Latest rules ni government office daggara verify cheyyandi.",
    "apply": "Kotha pension applications **ippudu open unnayo ledo** nenu verify cheyyalekapoyanu. Mee **Grama/Ward Sachivalayam** lo current process, dates confirm chesukondi. Aadhaar number or bank details ikkada share cheyyakandi.",
    "documents": "Required documents complete current list nenu official ga verify cheyyalekapoyanu. Apply cheyadam mundu official instructions leda mee **Grama/Ward Sachivalayam** daggara current list adugandi. Personal ID numbers ikkada share cheyyakandi.",
    "general": "Nenu Andhra Pradesh **NTR Bharosa old-age pension** gurinchi official information explain chestanu. **Age, pension amount, eligibility, documents, apply process** gurinchi adagandi. Source lekapothe guess cheyyanu.",
}


def classify(question: str) -> str:
    q = question.casefold().strip()
    # Age and amount phrases come before general eligibility terms.
    if re.search(r"\b(amount|how much|rupees|rs\.?|monthly|per month|ent[h]a|entha|pension entha)\b|ఎంత|రూపాయ", q):
        return "amount"
    if re.search(r"\b(age|years|60|vayasu|minimum age)\b|వయసు|ఏజ్", q):
        return "age"
    if re.search(r"\b(documents?|papers?|certificate|proof|documentlu)\b|డాక్యుమెంట్|పత్రాలు", q):
        return "documents"
    if re.search(r"\b(apply|application|register|deadline|last date|apply chey|apply ches|process)\b|దరఖాస్తు|అప్లై", q):
        return "apply"
    if re.search(r"\b(eligible|eligibility|qualify|conditions?|requirements?|vastunda|vasthunda|pension vas)\b|అర్హత|వస్తుందా|పెన్షన్", q):
        return "eligibility"
    return "general"


def contains_private_identifiers(question: str) -> bool:
    """Avoid sending likely identity/contact/banking details to an external AI API."""
    q = question.casefold()
    if re.search(r"\b(aadhaar|aadhar|bank account|account number|ifsc|pan number|otp|password)\b", q):
        return True
    # Catch pasted long ID/phone numbers, allowing spaces or hyphens.
    for candidate in re.findall(r"(?<!\w)[+\d][\d -]{8,22}\d(?!\w)", q):
        digits = re.sub(r"\D", "", candidate)
        if 10 <= len(digits) <= 18:
            return True
    return False


def fallback_answer(question: str, language: str = "Telugu") -> str:
    key = classify(question)
    return (TELUGU if language == "Telugu" else ENGLISH)[key]


def answer_question(question: str, language: str = "Telugu", api_key: str | None = None, model: str = "gemini-3.5-flash-lite") -> tuple[str, bool]:
    """Return (answer, used_model). With no key, use safe curated demo answers."""
    if contains_private_identifiers(question):
        warning = (
            "Please do not enter Aadhaar, bank, phone, OTP, or other private identifiers here. "
            "I can explain pension rules without these details."
            if language == "English" else
            "Aadhaar, bank, phone number, OTP lanti personal details ikkada ivvakandi. "
            "Ee details lekunda kuda pension rules explain chestanu."
        )
        return warning, False
    if not api_key:
        return fallback_answer(question, language), False
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""You are Janamitra AI, an Andhra Pradesh pension information assistant.
Use ONLY the FACTS below. No external knowledge or speculation.
Respond in {'simple Romanized Telugu' if language == 'Telugu' else 'simple English'}.
Answer the question clearly and briefly. If asked something not answered by FACTS,
say it cannot be verified and point the person to the official website or a local
Grama/Ward Sachivalayam. Do not claim final eligibility or application submission.
Never request Aadhaar numbers, account numbers, or other sensitive identifiers.
Do not invent citations, documents, URLs, deadlines, or pension amounts.

VERIFIED / QUALIFIED FACTS:\n{FACTS}\n
USER QUESTION:\n{question[:1200]}"""
        response = client.models.generate_content(model=model, contents=prompt)
        response_text = getattr(response, 'text', None)
        if response_text and response_text.strip():
            return response_text.strip(), True
    except Exception:
        pass  # Demo gracefully remains functional when free API quota is exceeded.
    return fallback_answer(question, language), False
