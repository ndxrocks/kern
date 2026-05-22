from typing import Union

from kern.session.agent import AgentSession
from kern.session.summary import SessionSummaryManager
from kern.session.team import TeamSession
from kern.session.workflow import WorkflowSession

Session = Union[AgentSession, TeamSession, WorkflowSession]

__all__ = ["AgentSession", "TeamSession", "WorkflowSession", "Session", "SessionSummaryManager"]
