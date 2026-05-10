import os


OUT_DIR = os.path.abspath("论文输出")
SVG_PATH = os.path.join(OUT_DIR, "学生成绩管理系统ER图.svg")


def entity(x, y, width, title, rows):
    header_h = 36
    row_h = 26
    height = header_h + row_h * len(rows)
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="#ffffff" stroke="#2f84bd" stroke-width="2"/>',
        f'<rect x="{x}" y="{y}" width="{width}" height="{header_h}" rx="8" fill="#2f84bd"/>',
        f'<text x="{x + width / 2}" y="{y + 24}" text-anchor="middle" class="title">{title}</text>',
    ]
    for index, row in enumerate(rows):
        row_y = y + header_h + index * row_h
        parts.append(f'<line x1="{x}" y1="{row_y}" x2="{x + width}" y2="{row_y}" stroke="#d8e0e7"/>')
        parts.append(f'<text x="{x + 14}" y="{row_y + 18}" class="field">{row}</text>')
    return "\n".join(parts), height


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    user, user_h = entity(80, 120, 260, "sys_user 用户表", [
        "PK id 用户编号",
        "username 登录账号",
        "password 登录密码",
        "enabled 是否启用",
    ])
    role, role_h = entity(860, 120, 260, "sys_role 角色表", [
        "PK id 角色编号",
        "name 角色标识",
        "description 角色说明",
    ])
    user_role, user_role_h = entity(470, 140, 270, "sys_user_role 用户角色表", [
        "PK/FK user_id 用户编号",
        "PK/FK role_id 角色编号",
    ])
    score, score_h = entity(385, 430, 440, "student_score 学生成绩表", [
        "PK id 成绩编号",
        "student_name 学生姓名",
        "student_number 学号",
        "subject 科目",
        "score 成绩",
        "exam_name 考试名称",
        "semester 学期",
        "exam_date 考试日期",
        "remark 备注",
    ])

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">
  <style>
    .page-title {{ font: 700 28px "Microsoft YaHei", Arial, sans-serif; fill: #23384d; }}
    .subtitle {{ font: 14px "Microsoft YaHei", Arial, sans-serif; fill: #607385; }}
    .title {{ font: 700 16px "Microsoft YaHei", Arial, sans-serif; fill: #ffffff; }}
    .field {{ font: 14px "Microsoft YaHei", Arial, sans-serif; fill: #23384d; }}
    .rel {{ font: 13px "Microsoft YaHei", Arial, sans-serif; fill: #496172; }}
    .line {{ stroke: #496172; stroke-width: 2.2; fill: none; marker-end: url(#arrow); }}
    .dash {{ stroke: #9aa9b5; stroke-width: 2; fill: none; stroke-dasharray: 8 6; }}
  </style>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#496172"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="1200" height="760" fill="#f4f7fb"/>
  <text x="600" y="46" text-anchor="middle" class="page-title">学生成绩管理系统 ER 图</text>
  <text x="600" y="74" text-anchor="middle" class="subtitle">用户、角色、用户角色关联与学生成绩数据结构</text>

  {user}
  {user_role}
  {role}
  {score}

  <path class="line" d="M340 190 C390 190, 420 190, 470 190"/>
  <text x="388" y="174" text-anchor="middle" class="rel">1</text>
  <text x="440" y="174" text-anchor="middle" class="rel">N</text>
  <text x="405" y="218" text-anchor="middle" class="rel">用户拥有角色关系</text>

  <path class="line" d="M740 190 C790 190, 810 190, 860 190"/>
  <text x="768" y="174" text-anchor="middle" class="rel">N</text>
  <text x="832" y="174" text-anchor="middle" class="rel">1</text>
  <text x="800" y="218" text-anchor="middle" class="rel">角色被用户引用</text>

  <path class="dash" d="M600 244 C600 310, 600 360, 600 430"/>
  <text x="624" y="342" class="rel">业务匹配：username 可对应 student_name</text>

  <rect x="74" y="666" width="1052" height="46" rx="6" fill="#ffffff" stroke="#d8e0e7"/>
  <text x="96" y="695" class="subtitle">说明：sys_user 与 sys_role 通过 sys_user_role 建立多对多关系；student_score 独立保存成绩业务数据，学生登录后可按姓名匹配定位成绩行。</text>
</svg>
'''
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(SVG_PATH)


if __name__ == "__main__":
    main()
