from abc import ABC, abstractmethod
from typing import List, Optional, Union

from fastapi import APIRouter

from kern.agent import Agent, RemoteAgent
from kern.team import RemoteTeam, Team
from kern.workflow import RemoteWorkflow, Workflow


class BaseInterface(ABC):
    type: str
    version: str = "1.0"
    agent: Optional[Union[Agent, RemoteAgent]] = None
    team: Optional[Union[Team, RemoteTeam]] = None
    workflow: Optional[Union[Workflow, RemoteWorkflow]] = None

    prefix: str
    tags: List[str]

    router: APIRouter

    @abstractmethod
    def get_router(self, use_async: bool = True, **kwargs) -> APIRouter:
        pass
