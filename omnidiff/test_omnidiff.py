from omnidiff import compare, get_jmespath
from omnidiff import map_jmespath
import jmespath
import unittest
import pprint


class TestOmnidiff(unittest.TestCase):
    def test_compare(self):
        dict1 = {
            "person": {
                "name": "Alice",
                "age": 30,
                "contact": {
                    "email": "alice@example.com",
                    "phone": ["123 - 456 - 7890", "098 - 765 - 4321"]
                },
                "hobbies": ["reading", "painting", "swimming"]
            },
            "work": {
                "company": "ABC Corp",
                "position": "Software Engineer",
                "projects": [
                    {
                        "name": "Project A",
                        "status": "Completed",
                        "team": ["Bob", "Charlie"]
                    },
                    {
                        "name": "Project B",
                        "status": "In Progress",
                        "team": ["David", "Eve"]
                    }
                ]
            },
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "zip": "10001"
            }
        }

        dict2 = {
            "person": {
                "name": "Alice",
                "age": 31,  # 年龄有变化
                "contact": {
                    "email": "alice_new@example.com",  # 邮箱有变化
                    "phone": ["123 - 456 - 7890", "555 - 5555"]  # 电话号码有变化
                },
                "hobbies": ["reading", "dancing", "swimming"]  # 爱好有变化
            },
            "work": {
                "company": "ABC Corp",
                "position": "Senior Software Engineer",  # 职位有变化
                "projects": [
                    {
                        "name": "Project A",
                        "status": "Archived",  # 项目状态有变化
                        "team": ["Bob", "Charlie", "Frank"]  # 团队成员有变化
                    },
                    {
                        "name": "Project C",  # 新增项目
                        "status": "Planned",
                        "team": ["Grace", "Henry"]
                    }
                ]
            },
            "address": {
                "street": "456 Elm St",  # 街道有变化
                "city": "New York",
                "zip": "10002"  # 邮编有变化
            }
        }

        compare_result = compare(dict1, dict2, [])

        expect_diff_fields = ['@.address.street',
                              '@.address.zip',
                              '@.person.age',
                              '@.person.contact.email',
                              '@.person.contact.phone[1]',
                              '@.person.hobbies[1]',
                              '@.work.position',
                              '@.work.projects[0].status',
                              '@.work.projects[1].name',
                              '@.work.projects[1].status',
                              '@.work.projects[1].team[0]',
                              '@.work.projects[1].team[1]'
                              ]

        for field in expect_diff_fields:
            assert field in [item[0] for item in compare_result.diff_fields]

        expect_a_missing_fields = ['@.work.projects[0].team[2]']
        for field in expect_a_missing_fields:
            assert field in [item[0] for item in compare_result.a_missing_fields]

    def test_map_jmespath(self):
        data = {
            "person": {
                "name": "Alice",
                "age": 31,  # 年龄有变化
                "contact": {
                    "email": "alice_new@example.com",  # 邮箱有变化
                    "phone": ["123 - 456 - 7890", "555 - 5555"]  # 电话号码有变化
                },
                "hobbies": ["reading", "dancing", "swimming"]  # 爱好有变化
            },
            "work": {
                "company": "ABC Corp",
                "position": "Senior Software Engineer",  # 职位有变化
                "projects": [
                    {
                        "name": "Project A",
                        "status": "Archived",  # 项目状态有变化
                        "team": ["Bob", "Charlie", "Frank"]  # 团队成员有变化
                    },
                    {
                        "name": "Project C",  # 新增项目
                        "status": "Planned",
                        "team": ["Grace", "Henry"]
                    }
                ]
            },
            "address": {
                "street": "456 Elm St",  # 街道有变化
                "city": "New York",
                "zip": "10002"  # 邮编有变化
            }
        }

        json = map_jmespath(data, '@.work.projects', lambda x: x['name'].replace(' ', ''))
        expect_path = ['@',
                       '@.person',
                       '@.person.name',
                       '@.person.age',
                       '@.person.contact',
                       '@.person.contact.email',
                       '@.person.contact.phone',
                       '@.person.contact.phone[0]',
                       '@.person.contact.phone[1]',
                       '@.person.hobbies',
                       '@.person.hobbies[0]',
                       '@.person.hobbies[1]',
                       '@.person.hobbies[2]',
                       '@.work',
                       '@.work.company',
                       '@.work.position',
                       '@.work.projects',
                       '@.work.projects.ProjectA',
                       '@.work.projects.ProjectA.name',
                       '@.work.projects.ProjectA.status',
                       '@.work.projects.ProjectA.team',
                       '@.work.projects.ProjectA.team[0]',
                       '@.work.projects.ProjectA.team[1]',
                       '@.work.projects.ProjectA.team[2]',
                       '@.work.projects.ProjectC',
                       '@.work.projects.ProjectC.name',
                       '@.work.projects.ProjectC.status',
                       '@.work.projects.ProjectC.team',
                       '@.work.projects.ProjectC.team[0]',
                       '@.work.projects.ProjectC.team[1]',
                       '@.address',
                       '@.address.street',
                       '@.address.city',
                       '@.address.zip']

        json_path = get_jmespath(json, [])
        for path in expect_path:
            assert path in json_path
        print(jmespath.search('@.work.projects.ProjectA', json))
