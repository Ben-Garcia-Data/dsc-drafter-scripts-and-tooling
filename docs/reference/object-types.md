# Drawing object types

Attributes of every drawing object type, read with `obj["Name"]` and written with `obj["Name"] = value`. Units are the public ones (see conventions.md): mm, plan Y up, degrees counter-clockwise, colours as "#RRGGBB". Unit "" means the value is passed through unchanged (flags, counts, enums, text).

## Actor

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `AssetDef` |  | Link |  |
| `AttributeOverrides` |  | String |  |
| `BlockColor` |  | Int |  |
| `BlockColorInherited` |  | Bool |  |

## Annotation

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `LeaderShape` |  | Int |  |
| `LeaderObjectEnd` |  | Int |  |
| `LeaderTagEnd` |  | Int |  |
| `LeaderTagAttach` |  | Int |  |
| `LeaderShoulder` |  | Float |  |
| `LeaderBend` |  | Vector |  |
| `LeaderMarkerSize` |  | Float |  |
| `LeaderAutoHide` |  | Bool |  |
| `LeaderStrokeColor` | colour | Int |  |
| `LeaderStrokeWidth` |  | Float |  |
| `LeaderStrokeStyle` |  | Int |  |
| `LeaderObjectGap` |  | Float |  |
| `Text` |  | String |  |
| `Shape` |  | Int |  |
| `TextHeight` | mm | Float |  |
| `BoxWidth` | mm | Float |  |
| `BoxHeight` | mm | Float |  |
| `LeaderTarget` | mm | Vector |  |
| `FontFamily` |  | String |  |
| `TextColor` | colour | Int |  |
| `BorderColor` | colour | Int |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |

## Arc

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Center` | mm | Vector |  |
| `Radius` | mm | Float |  |
| `StartAngle` | deg | Float |  |
| `EndAngle` | deg | Float |  |
| `MidParam` |  | Float |  |
| `FillMode` |  | Int |  |

## AssetInstance

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Representation2D` |  | Int |  |
| `SymbolAsset` |  | Link |  |
| `Model3DAssetId` |  | String |  |

## Circle

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Center` | mm | Vector |  |
| `Radius` | mm | Float |  |

## Composite

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |

## ComputedGeometry

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `Object2D` |  | Link |  |
| `Object3D` |  | Link |  |

## ConstructionLine

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Direction` | direction | Vector |  |
| `Infinite` |  | Bool |  |

## DataTag

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `TopLeft` | mm | Vector |  |
| `Width` | mm | Float |  |
| `Height` | mm | Float |  |
| `RichText` |  | String |  |
| `FontSize` |  | Float |  |
| `FontFamily` |  | String |  |
| `FontBold` |  | Bool |  |
| `FontItalic` |  | Bool |  |
| `FontUnderline` |  | Bool |  |
| `FontStrikethrough` |  | Bool |  |
| `TextColor` | colour | Int |  |
| `Alignment` |  | Int | Options: Left, Centre, Right, Justify |
| `ListType` |  | Int | Options: None, Ordered, Unordered |
| `VerticalAnchor` |  | Int | Options: Top, Middle, Bottom |
| `RunsMetadata` |  | String |  |
| `BlocksMetadata` |  | String |  |
| `IsDynamic` |  | Bool |  |
| `DynamicTag` |  | String |  |
| `DynamicPrompt` |  | String |  |
| `DynamicDefault` |  | String |  |
| `DynamicFlags` |  | Int |  |
| `TargetObject` |  | Link |  |
| `Viewport` |  | Link |  |
| `SourceObjectId` |  | String |  |
| `SourceInstanceId` |  | String |  |
| `FeatureId` |  | String |  |
| `SourceCoordinate` | mm | Vector |  |
| `AttachmentValid` |  | Bool |  |
| `AttributeName` |  | String |  |
| `FormatString` |  | String |  |
| `ShowLeader` |  | Bool |  |
| `TextOverridden` |  | Bool |  |
| `LineColor` | colour | Int |  |

## DataTagInstance

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `LeaderShape` |  | Int |  |
| `LeaderObjectEnd` |  | Int |  |
| `LeaderTagEnd` |  | Int |  |
| `LeaderTagAttach` |  | Int |  |
| `LeaderShoulder` | mm | Float |  |
| `LeaderBend` |  | Vector |  |
| `LeaderMarkerSize` | mm | Float |  |
| `LeaderAutoHide` |  | Bool |  |
| `LeaderStrokeColor` | colour | Int |  |
| `LeaderStrokeWidth` |  | Float |  |
| `LeaderStrokeStyle` |  | Int |  |
| `LeaderObjectGap` | mm | Float |  |
| `StyleLink` |  | Link |  |
| `TargetObject` |  | Link |  |
| `Viewport` |  | Link |  |
| `SourceObjectId` |  | String |  |
| `SourceInstanceId` |  | String |  |
| `FeatureId` |  | String |  |
| `AttachLocal` |  | Vector |  |
| `AttachmentValid` |  | Bool |  |
| `Placement` |  | Int |  |
| `TagOffset` |  | Vector |  |
| `TextUpright` |  | Bool |  |
| `TagScale` |  | Float |  |
| `OverrideKeys` |  | StringList |  |
| `OverrideValues` |  | StringList |  |
| `HiddenFields` |  | StringList |  |
| `BuiltStyleRevision` |  | Int |  |

## DimensionAligned

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `OverrideText` |  | String |  |
| `FontSize` |  | Float |  |
| `FontFamily` |  | String |  |
| `FontBold` |  | Bool |  |
| `FontItalic` |  | Bool |  |
| `FontUnderline` |  | Bool |  |
| `FontStrikethrough` |  | Bool |  |
| `TextColor` | colour | Int |  |
| `Alignment` |  | Int | Options: Left, Centre, Right, Justify |
| `ArrowSize` | mm | Float |  |
| `StrokeColor` | colour | Int |  |
| `Unit` |  | Int |  |
| `Precision` |  | Int |  |
| `MeasurementScale` |  | Float |  |
| `Rounding` | mm | Float |  |
| `TextPrefix` |  | String |  |
| `TextSuffix` |  | String |  |
| `SuppressTrailingZeros` |  | Bool |  |
| `TextOffset` | mm | Vector |  |
| `Endpoint1Viewport` |  | Link |  |
| `Endpoint1SourceObjectId` |  | String |  |
| `Endpoint1SourceInstanceId` |  | String |  |
| `Endpoint1FeatureId` |  | String |  |
| `Endpoint1SourceCoordinate` |  | Vector |  |
| `Endpoint1Valid` |  | Bool |  |
| `Endpoint2Viewport` |  | Link |  |
| `Endpoint2SourceObjectId` |  | String |  |
| `Endpoint2SourceInstanceId` |  | String |  |
| `Endpoint2FeatureId` |  | String |  |
| `Endpoint2SourceCoordinate` |  | Vector |  |
| `Endpoint2Valid` |  | Bool |  |
| `Point1` |  | Vector |  |
| `Point2` |  | Vector |  |
| `LinePoint` | mm | Vector |  |
| `DimLineAngle` | deg | Float |  |
| `ExtLine1` |  | Link |  |
| `ExtLine2` |  | Link |  |
| `DimLine` |  | Link |  |
| `Arrow1` |  | Link |  |
| `Arrow2` |  | Link |  |
| `Label` |  | Link |  |

## DimensionLinear

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `OverrideText` |  | String |  |
| `FontSize` |  | Float |  |
| `FontFamily` |  | String |  |
| `FontBold` |  | Bool |  |
| `FontItalic` |  | Bool |  |
| `FontUnderline` |  | Bool |  |
| `FontStrikethrough` |  | Bool |  |
| `TextColor` | colour | Int |  |
| `Alignment` |  | Int | Options: Left, Centre, Right, Justify |
| `ArrowSize` | mm | Float |  |
| `StrokeColor` | colour | Int |  |
| `Unit` |  | Int |  |
| `Precision` |  | Int |  |
| `MeasurementScale` |  | Float |  |
| `Rounding` | mm | Float |  |
| `TextPrefix` |  | String |  |
| `TextSuffix` |  | String |  |
| `SuppressTrailingZeros` |  | Bool |  |
| `TextOffset` | mm | Vector |  |
| `Endpoint1Viewport` |  | Link |  |
| `Endpoint1SourceObjectId` |  | String |  |
| `Endpoint1SourceInstanceId` |  | String |  |
| `Endpoint1FeatureId` |  | String |  |
| `Endpoint1SourceCoordinate` |  | Vector |  |
| `Endpoint1Valid` |  | Bool |  |
| `Endpoint2Viewport` |  | Link |  |
| `Endpoint2SourceObjectId` |  | String |  |
| `Endpoint2SourceInstanceId` |  | String |  |
| `Endpoint2FeatureId` |  | String |  |
| `Endpoint2SourceCoordinate` |  | Vector |  |
| `Endpoint2Valid` |  | Bool |  |
| `Point1` |  | Vector |  |
| `Point2` |  | Vector |  |
| `LinePoint` | mm | Vector |  |
| `DimLineAngle` | deg | Float |  |
| `ExtLine1` |  | Link |  |
| `ExtLine2` |  | Link |  |
| `DimLine` |  | Link |  |
| `Arrow1` |  | Link |  |
| `Arrow2` |  | Link |  |
| `Label` |  | Link |  |

## DimensionRadius

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `OverrideText` |  | String |  |
| `FontSize` |  | Float |  |
| `FontFamily` |  | String |  |
| `FontBold` |  | Bool |  |
| `FontItalic` |  | Bool |  |
| `FontUnderline` |  | Bool |  |
| `FontStrikethrough` |  | Bool |  |
| `TextColor` | colour | Int |  |
| `Alignment` |  | Int | Options: Left, Centre, Right, Justify |
| `ArrowSize` | mm | Float |  |
| `StrokeColor` | colour | Int |  |
| `Unit` |  | Int |  |
| `Precision` |  | Int |  |
| `MeasurementScale` |  | Float |  |
| `Rounding` | mm | Float |  |
| `TextPrefix` |  | String |  |
| `TextSuffix` |  | String |  |
| `SuppressTrailingZeros` |  | Bool |  |
| `TextOffset` | mm | Vector |  |
| `Endpoint1Viewport` |  | Link |  |
| `Endpoint1SourceObjectId` |  | String |  |
| `Endpoint1SourceInstanceId` |  | String |  |
| `Endpoint1FeatureId` |  | String |  |
| `Endpoint1SourceCoordinate` |  | Vector |  |
| `Endpoint1Valid` |  | Bool |  |
| `Endpoint2Viewport` |  | Link |  |
| `Endpoint2SourceObjectId` |  | String |  |
| `Endpoint2SourceInstanceId` |  | String |  |
| `Endpoint2FeatureId` |  | String |  |
| `Endpoint2SourceCoordinate` |  | Vector |  |
| `Endpoint2Valid` |  | Bool |  |
| `ArcPoint` | mm | Vector |  |
| `LeaderLength` | mm | Float |  |
| `RadialLine` |  | Link |  |
| `LeaderLine` |  | Link |  |
| `Arrow` |  | Link |  |
| `Label` |  | Link |  |

## Ellipse

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Semi-Major` |  | Float |  |
| `Semi-Minor` |  | Float |  |

## Equipment

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Representation2D` |  | Int |  |
| `SymbolAsset` |  | Link |  |
| `Model3DAssetId` |  | String |  |

## Group

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |

## Hatch

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Points` | mm | VectorList |  |
| `LoopSizes` |  | FloatList |  |

## Hoist

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `Object2D` |  | Link |  |
| `Object3D` |  | Link |  |
| `ChainEnd` | mm | Vector |  |

## Leader

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |

## LightingDevice

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `Pan` | deg | Float |  |
| `Tilt` | deg | Float |  |
| `PanMin` |  | Float |  |
| `PanMax` |  | Float |  |
| `TiltMin` |  | Float |  |
| `TiltMax` |  | Float |  |
| `PanJoint` |  | Link |  |
| `TiltJoint` |  | Link |  |
| `OrientFrame` |  | Link |  |
| `OrientMode` |  | Int |  |
| `StandUpright` |  | Bool |  |

## Line

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `StartPoint` | mm | Vector |  |
| `EndPoint` | mm | Vector |  |

## Pdf

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Width` | mm | Float |  |
| `Height` | mm | Float |  |
| `PageNumber` |  | Int |  |
| `SourceAssetId` |  | String |  |

## Point

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `MarkerSize` | mm | Float |  |

## Polyline

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Points` | mm | VectorList |  |
| `Bulges` |  | FloatList |  |

## Rectangle

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Corner1` |  | Vector |  |
| `Corner2` |  | Vector |  |

## RigMember

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `Object2D` |  | Link |  |
| `Object3D` |  | Link |  |
| `StartConnection` |  | Link |  |
| `EndConnection` |  | Link |  |

## ScaleBar

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `TotalLength` | mm | Float |  |
| `MajorInterval` | mm | Float |  |
| `MinorInterval` | mm | Float |  |
| `UnitFormat` |  | String |  |
| `BarHeight` | mm | Float |  |
| `TextHeight` | mm | Float |  |
| `FontFamily` |  | String |  |
| `PrimaryColor` | colour | Int |  |
| `SecondaryColor` | colour | Int |  |
| `LineColor` | colour | Int |  |
| `TextColor` | colour | Int |  |

## SceneObject2D3D

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `Object2D` |  | Link |  |
| `Object3D` |  | Link |  |

## SceneObject3D

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `MeshVertices` | mm | VectorList |  |
| `MeshEdges` |  | VectorList |  |
| `MeshAssetId` |  | String |  |
| `MeshFormat` |  | String |  |
| `MeshPartKey` |  | String |  |
| `PivotOffset` | mm | Vector |  |
| `MaterialColor` |  | Int |  |

## ScheduleTable

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `ScheduleTableGrid` |  | String |  |
| `ScheduleLink` |  | Link |  |
| `TextHeight` | mm | Float |  |
| `FontFamily` |  | String |  |
| `TextColor` | colour | Int |  |
| `LineColor` | colour | Int |  |
| `LineWidth` |  | Float |  |
| `BackgroundColor` | colour | Int |  |
| `HeaderBackground` | colour | Int |  |
| `MaxHeight` | mm | Float |  |
| `ShowHeader` |  | Bool |  |
| `RowLines` |  | Bool |  |
| `Zebra` |  | Bool |  |
| `ZebraColor` | colour | Int |  |
| `BuiltRowsPerCol` |  | Int |  |
| `BuiltFlowCols` |  | Int |  |
| `BuiltColCount` |  | Int |  |

## SoftGoods

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `Object2D` |  | Link |  |
| `Object3D` |  | Link |  |
| `GoodsWidth` | mm | Float |  |
| `Drop` | mm | Float |  |
| `Fullness` |  | Float |  |

## Speaker

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `Object2D` |  | Link |  |
| `Object3D` |  | Link |  |

## SpeakerArray

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `Object2D` |  | Link |  |
| `Object3D` |  | Link |  |

## Sphere

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Center` | mm | Vector |  |
| `Radius` | mm | Float |  |

## Spline

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `FitPts` | mm | VectorList |  |
| `BegTanVec` | direction | Vector |  |
| `EndTanVec` | direction | Vector |  |

## Stage

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `PlanObject` |  | Link |  |
| `DeckMesh` |  | Link |  |
| `LegsMesh` |  | Link |  |
| `RailingMesh` |  | Link |  |
| `FacadeMesh` |  | Link |  |

## Text

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `TopLeft` | mm | Vector |  |
| `Width` | mm | Float |  |
| `Height` | mm | Float |  |
| `RichText` |  | String |  |
| `FontSize` |  | Float |  |
| `FontFamily` |  | String |  |
| `FontBold` |  | Bool |  |
| `FontItalic` |  | Bool |  |
| `FontUnderline` |  | Bool |  |
| `FontStrikethrough` |  | Bool |  |
| `TextColor` | colour | Int |  |
| `Alignment` |  | Int | Options: Left, Centre, Right, Justify |
| `ListType` |  | Int | Options: None, Ordered, Unordered |
| `VerticalAnchor` |  | Int | Options: Top, Middle, Bottom |
| `RunsMetadata` |  | String |  |
| `BlocksMetadata` |  | String |  |
| `IsDynamic` |  | Bool |  |
| `DynamicTag` |  | String |  |
| `DynamicPrompt` |  | String |  |
| `DynamicDefault` |  | String |  |
| `DynamicFlags` |  | Int |  |

## TitleBlock

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `ProjectName` |  | String |  |
| `SheetTitle` |  | String |  |
| `SheetNumber` |  | String |  |
| `Revision` |  | String |  |
| `ScaleText` |  | String |  |
| `DateText` |  | String |  |
| `DrawnBy` |  | String |  |
| `CheckedBy` |  | String |  |
| `SheetLink` |  | Link |  |
| `LinkSheetName` |  | Bool |  |
| `TextHeight` | mm | Float |  |
| `FontFamily` |  | String |  |
| `TextColor` | colour | Int |  |
| `LineColor` | colour | Int |  |
| `BackgroundColor` | colour | Int |  |

## TitleBlockInstance

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `Children` |  | LinkList |  |
| `LayoutLink` |  | Link |  |
| `SheetLink` |  | Link |  |
| `RenderMode` |  | Int |  |
| `OverrideTokens` |  | StringList |  |
| `OverrideValues` |  | StringList |  |
| `Warnings` |  | StringList |  |
| `UsedTokens` |  | StringList |  |

## Viewport

| Attribute | Unit | Storage | Notes |
|---|---|---|---|
| `Label` |  | String |  |
| `Location` | mm | Vector |  |
| `Rotation` | deg | Vector |  |
| `Scale` |  | Vector |  |
| `Visible` |  | Bool |  |
| `Locked` |  | Bool |  |
| `DesignLayer` |  | Link |  |
| `ObjectType` |  | Link |  |
| `Department` |  | Link |  |
| `ParentGroup` |  | Link |  |
| `AttachParent` |  | Link |  |
| `ParentAsset` |  | Link |  |
| `StrokeColor` | colour | Int |  |
| `StrokeWidth` |  | Float |  |
| `StrokeStyle` |  | Int |  |
| `StrokeInherited` |  | Bool |  |
| `UseClassStrokeColor` |  | Bool |  |
| `FillColor` | colour | Int |  |
| `FillOpacity` |  | Float |  |
| `UseClassFillColor` |  | Bool |  |
| `FillType` |  | Int |  |
| `FillTextureId` |  | String |  |
| `FillTextureFit` |  | Int |  |
| `FillGradient` |  | String |  |
| `FillFilter` |  | String |  |
| `FillClip` |  | String |  |
| `IsClosed` |  | Bool |  |
| `StretchBehavior` |  | Int |  |
| `ExtrudeHeight` | mm | Float |  |
| `Width` | mm | Float |  |
| `Height` | mm | Float |  |
| `SourceScale` |  | Float |  |
| `DPI` |  | Float |  |
| `SourceCenter` | mm | Vector |  |
| `ShowLabel` |  | Bool |  |
| `SourceKind` |  | String |  |
| `Projection` |  | String |  |
| `RenderAs` |  | String |  |
| `CameraTarget` | mm | Vector |  |
| `CameraYaw` | deg | Float |  |
| `CameraPitch` | deg | Float |  |
| `CameraDistance` | mm | Float |  |
| `CameraRevision` |  | Int |  |
| `CropRevision` |  | Int |  |
| `BackgroundColor` | colour | Int |  |
| `DesignLayerVisibility` |  | String |  |
| `ObjectTypeVisibility` |  | String |  |
| `DepartmentVisibility` |  | String |  |
| `VisibleObjectIds` |  | String |  |
| `CropShape` |  | String |  |
| `CompletedScopeSnapshot` |  | String |  |
