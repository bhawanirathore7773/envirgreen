"""Business logic for issue status transitions.

Kept out of views/admin so that every status change goes through one
audited path, per docs/03-technical-architecture.md (Security section).
"""

from django.utils import timezone

from moderation.models import AuditLog
from .models import Issue, IssueUpdate

# Which statuses may legally follow which — blocks e.g. reported -> resolved
ALLOWED_TRANSITIONS = {
    "reported": {"verified", "no_action"},
    "verified": {"authority_identified", "escalated"},
    "authority_identified": {"reported_to_authority"},
    "reported_to_authority": {"followup_required", "action_taken"},
    "followup_required": {"action_taken", "escalated"},
    "action_taken": {"community_verified"},
    "community_verified": {"resolved"},
    "escalated": {"reported_to_authority", "action_taken"},
    "no_action": {"escalated"},
    "resolved": set(),
}


def transition_issue(issue: Issue, new_status: str, actor, note: str = "", photo=None) -> IssueUpdate:
    allowed = ALLOWED_TRANSITIONS.get(issue.status, set())
    if new_status not in allowed:
        raise ValueError(f"Cannot move issue from '{issue.status}' to '{new_status}'")

    issue.status = new_status
    issue.updated_at = timezone.now()
    issue.save(update_fields=["status", "updated_at"])

    update = IssueUpdate.objects.create(issue=issue, status=new_status, note=note, actor=actor, photo=photo)

    AuditLog.objects.create(
        actor=actor,
        action=f"issue.transition.{new_status}",
        object_repr=str(issue),
        metadata={"issue_id": issue.pk, "new_status": new_status},
    )
    return update
