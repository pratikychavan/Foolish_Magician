from mongoengine import Document, EmbeddedDocument, StringField, IntField, ListField, DictField, CachedReferenceField
from Database import BaseModel
from Database.auth import User

class UserDefinedFunction(BaseModel):
    user = CachedReferenceField(User)
    name = models.CharField(max_length=225)
    args = ArrayField(models.JSONField(null=True), default=list, blank=True)
    code = models.TextField(blank=True)
    tags = models.JSONField(null=True,default=tags_defaults)
    project_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    libraries = models.JSONField(default=list,null=True)
    source_details = models.JSONField(default=source_details_defaults)
    execution_details = models.JSONField(default=execution_details_defaults)
    execution_count = models.IntegerField(default=0, null=True)
    show_in_op_bar = models.BooleanField(default=False)
    github_integration = models.BooleanField(default=False)
    authored_by = models.CharField(max_length=255, null=True)
    miscellaneous = models.JSONField(default={})