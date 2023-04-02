from app.models import Department


def validate_department(dep) -> Department | None:
    return Department.query.filter(Department.name == dep.replace("_", " ")).first()