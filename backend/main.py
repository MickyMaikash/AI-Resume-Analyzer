from fastapi import FastAPI, UploadFile, File, HTTPException,Form
from pydantic import BaseModel
from typing import Dict,List,Any
import json
from analyzer import pdfTextSplitter,analyzerResume
import os
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"]
)
@app.get("/")
def set_msg():
    return {"mesg":"App Started Successfully"}


@app.post("/analyze")
async def analyze_pdf( resume: UploadFile = File(...),
        job_des: str = Form(...)):
    try:
        print("Analyze pdf requerst recieved")
        if resume.content_type!="application/pdf":
            raise HTTPException(
                status_code=401,
                detail="Only PDF files are allowed"
            )

        if not job_des:
            raise HTTPException(
                status_code=404,
                detail="job description should not be empty"
            )
        data = await resume.read()

        path="temp.pdf"
        with open(path, "wb") as f:
            f.write(data)
        extractedTxt=pdfTextSplitter(path)

        if not extractedTxt:
            raise HTTPException(
                status_code=403,
                detail="Please Send Valid Pdf File"
            )

        result=analyzerResume(resume=extractedTxt,job_des=job_des)
        if not result:
            return {"message":"Something Went wrong while analayzing your reusme"}

        print(f"The Analyze the result is {result}")
        jsonResult=json.loads(result)
        return jsonResult
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail="Please Send Valid Pdf File"
            )
    finally:
        if os.path.exists(path):
            os.remove(path)

    

    
