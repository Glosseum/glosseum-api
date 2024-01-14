from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, event
from sqlalchemy.orm import relationship
from data.db.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Board(Base):
    __tablename__ = "board"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)
    description = Column(String)

    creator_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    creator = relationship("User", backref="boards")


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)
    content = Column(String)

    creator_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    creator = relationship("User", backref="articles")

    board_id = Column(Integer, ForeignKey("board.id", onupdate="CASCADE", ondelete="CASCADE"))
    board = relationship("Board", backref="articles")

    # Article 간 트리 구조를 구현하기 위해 Path Enumeration 디자인 패턴 사용 (보드 조회 시 모든 아티클 조회하므로 순환 연산의 부담이 없음)
    # https://stackoverflow.com/questions/4048151/path-enumeration-design-pattern
    # board_id/parent_id/parent_id/parent_id/.../article_id -> 32/1/6/9 형태로 저장
    # path_logical 에서 board_id/agree/agree/disagree.. 와 같이 논리 구조를 표현

    path = Column(String, index=True)
    path_logical = Column(String)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)

    content = Column(String)

    creator_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    creator = relationship("User", backref="comments")

    article_id = Column(Integer, ForeignKey("article.id", onupdate="CASCADE", ondelete="CASCADE"))
    article = relationship("Article", backref="comments")
