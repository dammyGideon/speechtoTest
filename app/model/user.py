from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel) :
    id: int  = Field (default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)
    class config:
        schema_extra = {
            "post_demo" :  {
                "title":"Some title about posting",
                "content":"some content about posting"
            }
        }