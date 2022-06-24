"""
Data structures to interact with discussions and pull requests on the Hub.

See [the discussions and pull requests guide](https://huggingface.co/docs/hub/repositories-pull-requests-discussions)
for more information on pull requests, discussions, and the community tab.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from dateutil.parser import parse as parse_datetime


@dataclass
class Discussion:
    """
    A discussion or pull request on the Hub.

    Attributes:
        title (`str`):
            The title of the discussion / pull request
        status (`str`):
            The status of the discussion / pull request.
            It can be one of:
                * `"open"`
                * `"closed"`
                * `"merged"` (only for pull requests)
                * `"draft"` (only for pull requests)
        num (`int`):
            The number of the discussion / pull request.
        repo_id (`str`):
            The id (`"{namespace}/{repo_name}"`) of the repo on which
            the discussion / pull request was open.
        repo_type (`str`):
            The type of the repo on which the discussion / pull request was open.
            Posiible values are: `"model"`, `"dataset"`, `"space"`.
        author (`str`):
            The username of the discussion / pull request author.
            Can be `"deleted"` if the user has been deleted since.
        is_pull_request (`bool`):
            Wether or not this is a pull request.
        created_at (`datetime`):
            The `datetime` of creation of the discussion / pull request.
    """

    title: str
    status: str
    num: int
    repo_id: str
    repo_type: str
    author: str
    is_pull_request: bool
    created_at: datetime


@dataclass
class DiscussionWithDetails(Discussion):
    """
    Subclass of [`Discussion`].

    Attributes:
        title (`str`):
            The title of the discussion / pull request
        status (`str`):
            The status of the discussion / pull request.
            It can be one of:
                * `"open"`
                * `"closed"`
                * `"merged"` (only for pull requests)
                * `"draft"` (only for pull requests)
        num (`int`):
            The number of the discussion / pull request.
        repo_id (`str`):
            The id (`"{namespace}/{repo_name}"`) of the repo on which
            the discussion / pull request was open.
        repo_type (`str`):
            The type of the repo on which the discussion / pull request was open.
            Posiible values are: `"model"`, `"dataset"`, `"space"`.
        author (`str`):
            The username of the discussion / pull request author.
            Can be `"deleted"` if the user has been deleted since.
        is_pull_request (`bool`):
            Wether or not this is a pull request.
        created_at (`datetime`):
            The `datetime` of creation of the discussion / pull request.
        events (`list` of [`DiscussionEvent`])
            The list of [`DiscussionEvents`] in this discussion or pull request.
        conflicting_files (`list` of `str`, *optional*):
            A list of conflicting files if this is a pull request.
            `None` if `self.is_pull_request` is `False`.
        target_branch (`str`, *optional*):
            The branch into which changes are to be merged if this is a
            pull request. `None`  if `self.is_pull_request` is `False`.
        merge_commit_oid (`str`, *optional*):
            If this is a merged pull request, this is set to the OID / SHA of
            the merge commit, `None` otherwise.
        diff (`str`, *optional*):
            The git diff if this is a pull request, `None` otherwise.
    """

    events: List["DiscussionEvent"]
    conflicting_files: Optional[List[str]]
    target_branch: Optional[str]
    merge_commit_oid: Optional[str]
    diff: Optional[str]


@dataclass
class DiscussionEvent:
    """
    An event in a discussion or pull request.

    Use concrete classes:
        * [`DiscussionComment`]
        * [`DiscussionStatusChange`]
        * [`DiscussionCommit`]
        * [`DiscussionTitleChange`]

    Attributes:
        id (`str`):
            The ID of the event. An hexadecimal string.
        type (`str`):
            The type of the event.
        created_at (`datetime`):
            A [`datetime`](https://docs.python.org/3/library/datetime.html?highlight=datetime#datetime.datetime)
            object holding the creation timestamp for the event.
        author (`str`):
            The username of the discussion / pull request author.
            Can be `"deleted"` if the user has been deleted since.
    """

    id: str
    type: str
    created_at: datetime
    author: str

    _event: dict
    """Stores the original event data, in case we need to access it later"""


@dataclass
class DiscussionComment(DiscussionEvent):
    """A comment in a discussion / pull request.

    Subclass of [`DiscussionEvent`].


    Attributes:
        id (`str`):
            The ID of the event. An hexadecimal string.
        type (`str`):
            The type of the event.
        created_at (`datetime`):
            A [`datetime`](https://docs.python.org/3/library/datetime.html?highlight=datetime#datetime.datetime)
            object holding the creation timestamp for the event.
        author (`str`):
            The username of the discussion / pull request author.
            Can be `"deleted"` if the user has been deleted since.
        content (`str`):
            The raw markdown content of the comment. Mentions, links and images are not rendered.
        edited (`bool`):
            Wether or not this comment has been edited
        hidden (`bool`):
            Whether or not this comment has been hidden
    """

    content: str
    edited: bool
    hidden: bool

    # TODO @SBrandeis: implement methods to navigate comment history


@dataclass
class DiscussionStatusChange(DiscussionEvent):
    """A change of status in a discussion / pull request.

    Subclass of [`DiscussionEvent`].

    Attributes:
        id (`str`):
            The ID of the event. An hexadecimal string.
        type (`str`):
            The type of the event.
        created_at (`datetime`):
            A [`datetime`](https://docs.python.org/3/library/datetime.html?highlight=datetime#datetime.datetime)
            object holding the creation timestamp for the event.
        author (`str`):
            The username of the discussion / pull request author.
            Can be `"deleted"` if the user has been deleted since.
        new_status (`str`):
            The status of the discussion / pull request after the change.
            It can be one of:
                * `"open"`
                * `"closed"`
                * `"merged"` (only for pull requests)
    """

    new_status: str


@dataclass
class DiscussionCommit(DiscussionEvent):
    """A commit in a pull request.

    Subclass of [`DiscussionEvent`].

    Attributes:
        id (`str`):
            The ID of the event. An hexadecimal string.
        type (`str`):
            The type of the event.
        created_at (`datetime`):
            A [`datetime`](https://docs.python.org/3/library/datetime.html?highlight=datetime#datetime.datetime)
            object holding the creation timestamp for the event.
        author (`str`):
            The username of the discussion / pull request author.
            Can be `"deleted"` if the user has been deleted since.
        summary (`str`):
            The summary of the commit.
        oid (`str`):
            The OID / SHA of the commit, as a hexadecimal string.
    """

    summary: str
    oid: str


@dataclass
class DiscussionTitleChange(DiscussionEvent):
    """A rename event in a discussion / pull request.

    Subclass of [`DiscussionEvent`].

    Attributes:
        id (`str`):
            The ID of the event. An hexadecimal string.
        type (`str`):
            The type of the event.
        created_at (`datetime`):
            A [`datetime`](https://docs.python.org/3/library/datetime.html?highlight=datetime#datetime.datetime)
            object holding the creation timestamp for the event.
        author (`str`):
            The username of the discussion / pull request author.
            Can be `"deleted"` if the user has been deleted since.
        old_title (`str`):
            The previous title for the discussion / pull request
        new_title (`str`):
            The new title
    """

    old_title: str
    new_title: str


def deserialize_event(event: dict) -> DiscussionEvent:
    """Instantiates a [`DiscussionEvent`] from a dict"""
    event_id: str = event["id"]
    event_type: str = event["type"]
    created_at = parse_datetime(event["createdAt"])

    common_args = dict(
        id=event_id,
        type=event_type,
        created_at=created_at,
        author=event.get("author", {}).get("name", "deleted"),
        _event=event,
    )

    if event_type == "comment":
        return DiscussionComment(
            **common_args,
            edited=event["data"]["edited"],
            hidden=event["data"]["hidden"],
            content=event["data"]["latest"]["raw"],
        )
    if event_type == "status-change":
        return DiscussionStatusChange(
            **common_args,
            new_status=event["data"]["status"],
        )
    if event_type == "commit":
        return DiscussionCommit(
            **common_args,
            summary=event["data"]["subject"],
            oid=event["data"]["oid"],
        )
    if event_type == "title-change":
        return DiscussionTitleChange(
            **common_args,
            old_title=event["data"]["from"],
            new_title=event["data"]["to"],
        )

    return DiscussionEvent(**common_args)
