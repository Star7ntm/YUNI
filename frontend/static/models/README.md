# 3D模型文件目录

请将您的3D模型文件（GLB格式）放在此目录下。

## 支持的格式

- **GLB**（推荐）：单文件二进制格式，包含模型、纹理和材质
- **glTF**：JSON格式，需要外部资源文件

## 使用方法

1. 将您的模型文件（例如：`my-model.glb`）放入此目录
2. 在 `MainInterface.html` 中修改模型路径：
   ```html
   <model-viewer 
       src="/static/models/my-model.glb"
       ...
   ></model-viewer>
   ```

## 模型转换工具

- **Blender**：免费3D建模软件，可导出GLB格式
- **glTF-Pipeline**：命令行工具，用于优化和转换模型
- **在线转换器**：https://products.aspose.app/3d/conversion

## 示例模型

您可以从以下网站下载免费的示例模型：
- https://sketchfab.com/3d-models?features=downloadable&sort_by=-likeCount
- https://polyhaven.com/models

## 注意事项

- 模型文件大小建议控制在 10MB 以内，以确保快速加载
- 使用 GLB 格式可以获得更好的性能
- 如果模型较大，考虑使用压缩工具优化

