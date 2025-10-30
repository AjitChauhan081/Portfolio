## 🚀 **Website Performance Improvement Summary**

---

<table style="width:100%; border-collapse: collapse;">
    <thead>
        <tr style="background-color: #f2f2f2;">
            <th colspan="2" style="border: 1px solid #ddd; padding: 12px; text-align: left; font-size: 1.1em;">Project Overview: Post-Deployment Optimization</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold; width: 30%;">Initial Challenge</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Significant performance issues identified in **static files, templates, and database configuration** after initial deployment.</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">Performance Goal</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Improve the mobile **PageSpeed Insights** score from an initial $30-35$.</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">✅ Current Result</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Mobile performance score is now **around 60**.</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">🔗 PageSpeed Report</td>
            <td style="border: 1px solid #ddd; padding: 8px;"><a href="https://pagespeed.web.dev/analysis/https-ajitchauhan31-pythonanywhere-com/1kzmn4ev1p?hl=en-US&form_factor=mobile" target="_blank">Mobile PageSpeed Analysis</a></td>
        </tr>
    </tbody>
</table>

### 🛠️ **Optimization Techniques Implemented**

* **Image Optimization:**
    * **Lazy Loading:** Implemented native lazy loading for images to prioritize above-the-fold content.
    * **Use Django Stactic file hashing:** Implemented Django Static File Cashing library to incress the performance.
    * **Size Compression:** Compressed unnecessarily large images (some initially $>5\text{MB}$) to reduce payload.
    * **Format Change:** Converted existing **PNG** images to **WebP** format for better compression and superior performance.
* **Asset Loading:** Used the **`defer`** attribute for JavaScript files to prevent blocking of the initial page render.
* **Visual Effects:** Decreased the particle values in background effects to ensure a lighter overall payload.

### 💡 **Future Learning & Conclusion**

This deployment experience was crucial, as performance issues (especially **mobile-specific slowness**) were not visible during local development. This strongly emphasized the need for using **lightweight and highly optimized libraries** in all future projects.
