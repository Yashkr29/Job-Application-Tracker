from fastapi import UploadFile


class StorageService:
    """Supabase Storage adapter placeholder."""

    async def upload_resume(self, user_id: str, file: UploadFile) -> str:
        """Return the storage path where a resume would be uploaded."""
        safe_name = file.filename or "resume.pdf"
        return f"resumes/{user_id}/{safe_name}"


storage_service = StorageService()

