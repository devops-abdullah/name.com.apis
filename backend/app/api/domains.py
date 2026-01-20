from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.domain import Domain, CreateDNSRecord, UpdateDNSRecord, DomainWithRecords
from app.services.domain import domain_service
from app.services.dns import dns_service
from app.services.namecom import namecom_service
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/domains", tags=["domains"])

@router.get("", response_model=List[Domain])
async def list_domains(current_user: dict = Depends(get_current_user)):
    """List all domains"""
    try:
        namecom_domains = namecom_service.get_domains()
        return [{"name": d["domainName"], "namecom_id": d["domainId"]} for d in namecom_domains]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching domains: {str(e)}"
        )

@router.get("/{domain_name}", response_model=DomainWithRecords)
async def get_domain_details(domain_name: str, current_user: dict = Depends(get_current_user)):
    """Get domain details with DNS records"""
    try:
        domain_info = namecom_service.get_domain(domain_name)
        records = namecom_service.get_dns_records(domain_name)
        
        return {
            "name": domain_info.get("domainName"),
            "namecom_id": domain_info.get("domainId"),
            "team_id": 1,  # Should come from context
            "records": [
                {
                    "id": r.get("recordId"),
                    "domain": domain_name,
                    "name": r.get("name"),
                    "type": r.get("type"),
                    "content": r.get("answer"),
                    "ttl": r.get("ttl"),
                    "priority": r.get("mxPriority")
                }
                for r in records
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching domain details: {str(e)}"
        )

@router.post("/{domain_name}/records", response_model=dict)
async def create_dns_record(
    domain_name: str,
    record: CreateDNSRecord,
    current_user: dict = Depends(get_current_user)
):
    """Create DNS record"""
    try:
        result = namecom_service.create_dns_record(
            domain_name=domain_name,
            name=record.name,
            type=record.type,
            content=record.content,
            ttl=record.ttl,
            priority=record.priority
        )
        return {"message": "DNS record created successfully", "record": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating DNS record: {str(e)}"
        )

@router.get("/{domain_name}/records", response_model=List[dict])
async def list_dns_records(domain_name: str, current_user: dict = Depends(get_current_user)):
    """List DNS records for domain"""
    try:
        records = namecom_service.get_dns_records(domain_name)
        return [
            {
                "id": r.get("recordId"),
                "name": r.get("name"),
                "type": r.get("type"),
                "content": r.get("answer"),
                "ttl": r.get("ttl"),
                "priority": r.get("mxPriority")
            }
            for r in records
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching DNS records: {str(e)}"
        )

@router.put("/{domain_name}/records/{record_id}", response_model=dict)
async def update_dns_record(
    domain_name: str,
    record_id: int,
    record_update: UpdateDNSRecord,
    current_user: dict = Depends(get_current_user)
):
    """Update DNS record"""
    try:
        result = namecom_service.update_dns_record(
            domain_name=domain_name,
            record_id=record_id,
            content=record_update.content,
            ttl=record_update.ttl,
            priority=record_update.priority
        )
        return {"message": "DNS record updated successfully", "record": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating DNS record: {str(e)}"
        )

@router.delete("/{domain_name}/records/{record_id}")
async def delete_dns_record(
    domain_name: str,
    record_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete DNS record"""
    try:
        namecom_service.delete_dns_record(domain_name, record_id)
        return {"message": "DNS record deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting DNS record: {str(e)}"
        )
