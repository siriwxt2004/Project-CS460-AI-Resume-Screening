import google.generativeai as genai
import json
import re


def analyze(
    api_key,
    jd,
    candidates
):

    genai.configure(
        api_key=api_key
    )

    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )

    output = []

    for r in candidates:

        prompt = f"""

You are HR.

Evaluate candidate.

JOB:
{jd}

RESUME:
{r["content"]}

Return JSON only

{{
"score":0,
"verdict":"",
"reasoning":"",
"key_skills":[],
"missing_skills":[]
}}

"""

        try:

            res = model.generate_content(
                prompt
            )

            txt = re.search(
                r'\{.*\}',
                res.text,
                re.DOTALL
            ).group()

            obj = json.loads(
                txt
            )

            obj[
                "name"
            ] = r[
                "name"
            ]

            obj[
                "content"
            ] = r[
                "content"
            ]

            output.append(
                obj
            )

        except:

            continue

    return output