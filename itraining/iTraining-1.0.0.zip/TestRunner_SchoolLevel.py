# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, time, re, sys
import HTMLTestRunner
sys.path.append("..")
# print sys.path
from test_case.case_AnnualPlanAdd import AnnualPlanAdd
from test_case.case_AnnualPlanManagement import AnnualPlanManagement
from test_case.case_CoursePlanAdd import CoursePlanAdd
from test_case.case_SchoolLevelCoursePlanManagement import SchoolLevelCoursePlanManagement
from test_case.case_SchoolLevelCoursePlanApproval import SchoolLevelCoursePlanApproval
from test_case.case_SchoolLevelCourseActualize import SchoolLevelCourseActualize
from test_case.case_SchoolLevelHourApproval import SchoolLevelHourApproval
from test_case.case_SchoolLevelHourRecord import SchoolLevelHourRecord

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":

    suite = unittest.TestSuite()

    suite.addTest(AnnualPlanAdd("test_case_AnnualPlanAdd_SchoolLevel_003"))

    suite.addTest(AnnualPlanManagement("test_case_SearchAnnualPlan_001"))
    suite.addTest(AnnualPlanManagement("test_case_PublishAnnualPlan_002"))

    suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_SchoolLevel_Uniform_008"))
    suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_SchoolLevel_Own_009"))

    suite.addTest(SchoolLevelCoursePlanManagement("test_case_SchoolLevel_SearchCoursePlan_001"))
    suite.addTest(SchoolLevelCoursePlanManagement("test_case_SchoolLevel_ViewCoursePlan_002"))
    suite.addTest(SchoolLevelCoursePlanManagement("test_case_SchoolLevel_PublishCoursePlan_003"))
    suite.addTest(SchoolLevelCoursePlanManagement("test_case_SchoolLevel_EditCoursePlan_004"))
    suite.addTest(SchoolLevelCoursePlanManagement("test_case_SchoolLevel_DeleteCoursePlan_005"))

    suite.addTest(SchoolLevelCoursePlanApproval("test_case_Search_School_001"))
    suite.addTest(SchoolLevelCoursePlanApproval("test_case_UniformCourse_Approval_002"))
    suite.addTest(SchoolLevelCoursePlanApproval("test_case_OwnCourse_Approval_003"))

    suite.addTest(SchoolLevelCourseActualize("test_case_Search_Course_001"))
    suite.addTest(SchoolLevelCourseActualize("test_case_UniformCourse_Actualize_002"))
    suite.addTest(SchoolLevelCourseActualize("test_case_OwnCourse_Actualize_003"))

    suite.addTest(SchoolLevelHourRecord("test_case_Search_Course_001"))
    suite.addTest(SchoolLevelHourRecord("test_case_UniformCourse_HourRecord_002"))
    suite.addTest(SchoolLevelHourRecord("test_case_OwnCourse_HourRecord_003"))
    suite.addTest(SchoolLevelHourRecord("test_case_HourRecord_FieldVerification_004"))    

    suite.addTest(SchoolLevelHourApproval("test_case_Search_Course_001"))
    suite.addTest(SchoolLevelHourApproval("test_case_UniformCourse_HourApproval_002"))
    suite.addTest(SchoolLevelHourApproval("test_case_OwnCourse_HourApproval_003"))

    currenttime = time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time()))
    filename = 'D:\\iTraining\\result\\reports\\'+currenttime+'results.html'
    fp=file(filename,'wb')
    runner=HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=u'校级自动化测试报告',
            description=u'校级自动化测试报告'
    )
    runner.run(suite)
    fp.close()