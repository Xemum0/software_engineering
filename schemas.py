from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[
        validate.Length(min=8),
        validate.Regexp(r"(?=.*[A-Z])(?=.*\d)", error="Password must include at least one uppercase letter and one number")
    ])
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    phone = fields.String(validate=validate.Regexp(r"^\+?[1-9]\d{1,14}$", error="Invalid phone number format"), allow_none=True)
    role = fields.String()
    company_id = fields.String()
    branch_id = fields.String()
    avatar = fields.String()

    
