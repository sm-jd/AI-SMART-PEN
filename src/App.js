import { useState } from "react";
import OpenAI from "openai";

const openai = new OpenAI(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);
function App() {
    const [image, setImage] = useState(null);
    const [result, setResult] = useState("");
    const [loading, setLoading] = useState(false);

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        if (!file||!file.type.startsWith("image/")) {
            alert("Please upload an image file only.");
            return;
        }
        setImage(file);
    }
};
    const handleSubmit = async () => {
        if (!image) return;
        setLoading(true);
        setResult("");}
const response = await openai.responses.create({
      model: "gpt-4.1-mini",
      input: [
        {
          role: "user",
          content: [
            { type: "input_text", text: "Extract text from this image" },
            {
              type: "input_image",
              image_url: URL.createObjectURL(image),
            },
          ],
        },
      ],
    });

    setResult(response.output_text);
    setLoading(false);
  

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Image to Text Converter</h2>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
      />

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Processing..." : "Convert Image to Text"}
      </button>

      <br /><br />

      {result && (
        <div>
          <h3>Result:</h3>
          <p>{result}</p>
        </div>
 )}
    </div>
  );


export default App;
















































































































































        