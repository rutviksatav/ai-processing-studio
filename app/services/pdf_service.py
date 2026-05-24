import asyncio

from pypdf import PdfReader


async def extract_pdf_text(
    file_path: str
):

    def _extract():
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    return await asyncio.to_thread(_extract)
