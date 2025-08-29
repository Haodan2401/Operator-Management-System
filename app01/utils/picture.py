from PIL import Image, ImageDraw, ImageFont
import random
import string


def generate_captcha():
    # 生成4个随机字母（大写）
    captcha_text = ''.join(random.choices(string.ascii_uppercase, k=4))

    # 增大图片尺寸
    width, height = 180, 60
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    try:
        # 增大字体大小
        font = ImageFont.truetype("arial.ttf", 32)  # 从15增大到32
    except:
        try:
            # 尝试其他字体
            font = ImageFont.truetype("Arial Bold.ttf", 32)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
            except:
                # 如果找不到字体，使用默认字体但手动调整间距
                font = ImageFont.load_default()
                # 对于默认字体，我们需要分别绘制每个字符来增加间距

    # 分别绘制每个字符以增加间距
    char_spacing = 8  # 字符间距
    total_text_width = 0

    # 计算每个字符的宽度
    char_widths = []
    for char in captcha_text:
        if hasattr(font, 'getsize'):
            char_width = font.getsize(char)[0]
        else:
            char_width = 20  # 默认估算
        char_widths.append(char_width)
        total_text_width += char_width + char_spacing

    total_text_width -= char_spacing  # 最后一个字符不需要间距

    # 计算起始位置
    x = (width - total_text_width) / 2
    y = (height - 32) / 2  # 估算高度

    # 添加一些干扰线和噪点
    for i in range(5):
        # 随机干扰线
        draw.line(
            (random.randint(0, width), random.randint(0, height),
             random.randint(0, width), random.randint(0, height)),
            fill=(random.randint(150, 200), random.randint(150, 200), random.randint(150, 200)),
            width=1
        )

    for i in range(80):
        # 随机噪点
        draw.point(
            (random.randint(0, width), random.randint(0, height)),
            fill=(random.randint(150, 200), random.randint(150, 200), random.randint(150, 200))
        )

    # 分别绘制每个字符
    for i, char in enumerate(captcha_text):
        draw.text((x, y), char, font=font, fill=(0, 0, 0))
        x += char_widths[i] + char_spacing

    return image, captcha_text


# 测试代码
if __name__ == "__main__":
    image, text = generate_captcha()
    print(f"验证码: {text}")
    image.show()
    image.save("captcha.png")