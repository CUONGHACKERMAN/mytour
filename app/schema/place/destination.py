
# class Destination(TourBase, DomainBaseModel):
#     __tablename__ = "destination"

#     id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
#     name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
#     country: Mapped[str] = mapped_column(String(100), nullable=False)

#     templates: Mapped[List["TourTemplate"]] = relationship(
#         secondary=template_destination_assoc, back_populates="destinations"
#     )
