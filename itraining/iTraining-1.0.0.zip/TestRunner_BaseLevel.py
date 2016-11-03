# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, time, re, sys
import HTMLTestRunner
sys.path.append("..")
from test_case.case_AnnualPlanAdd import AnnualPlanAdd
from test_case.case_AnnualPlanManagement import AnnualPlanManagement
from test_case.case_CoursePlanAdd import CoursePlanAdd
from test_case.case_BaseLevelCoursePlanManagement import BaseLevelCoursePlanManagement
from test_case.case_BaseLevelCourseContentAdd import BaseLevelCourseContentAdd
from test_case.case_BaseLevelCourseRegistation import BaseLevelCourseRegistation
from test_case.case_BaseLevelCourseRegistationApproval import BaseLevelCourseRegistationApproval
from test_case.case_BaseLevelCourseActualize import BaseLevelCourseActualize
from test_case.case_BaseLevelCourseEvaluate import BaseLevelCourseEvaluate
from test_case.case_BaseLevelCourseStudy import BaseLevelCourseStudy
from test_case.case_BaseLevelCourseHourIdentify import BaseLevelCourseHourIdentify
from test_case.case_BaseLevelRequirmentSurveySummary import BaseLevelRequirmentSurveySummary

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(AnnualPlanAdd("test_case_AnnualPlanAdd_BaseLevel_002"))

    suite.addTest(AnnualPlanManagement("test_case_SearchAnnualPlan_001"))
    suite.addTest(AnnualPlanManagement("test_case_PublishAnnualPlan_002"))

    suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_BaseLevel_RealTime_005"))
    suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_BaseLevel_NotRealTime_006"))
    suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_BaseLevel_NotNetwork_007"))

    suite.addTest(BaseLevelCoursePlanManagement("test_case_BaseLevel_SearchCoursePlan_001"))
    suite.addTest(BaseLevelCoursePlanManagement("test_case_BaseLevel_PublishCoursePlan_002"))
    suite.addTest(BaseLevelCoursePlanManagement("test_case_BaseLevel_EditCoursePlan_003"))
    suite.addTest(BaseLevelCoursePlanManagement("test_case_BaseLevel_DeleteCoursePlan_004"))

    suite.addTest(BaseLevelCourseContentAdd("test_case_RealTime_AddCourseDesign_001"))
    suite.addTest(BaseLevelCourseContentAdd("test_case_NotRealTime_AddCourseDesign_002"))
    suite.addTest(BaseLevelCourseContentAdd("test_case_NotNetwork_AddCourseContent_003"))

    suite.addTest(BaseLevelCourseRegistation("test_case_SearchCourse_Registation_001"))
    suite.addTest(BaseLevelCourseRegistation("test_case_ViewCourse_Registation_002"))
    suite.addTest(BaseLevelCourseRegistation("test_case_Comfirm_Registation_003"))
    suite.addTest(BaseLevelCourseRegistation("test_case_Comfirm_Registation_004"))
    suite.addTest(BaseLevelCourseRegistation("test_case_School_Recommend_005"))

    suite.addTest(BaseLevelCourseRegistationApproval("test_case_BaseLevel_SearchApprovalRegistation_001"))
    suite.addTest(BaseLevelCourseRegistationApproval("test_case_BaseLevel_ApproveRegistation_002"))
    suite.addTest(BaseLevelCourseRegistationApproval("test_case_BaseLevel_ApproveRegistation_003"))
    suite.addTest(BaseLevelCourseRegistationApproval("test_case_BaseLevel_ApproveRegistation_004"))
    
    suite.addTest(BaseLevelCourseActualize("test_case_RealTime_ViewInformation_001"))
    suite.addTest(BaseLevelCourseActualize("test_case_RealTime_AssignHomework_002"))
    suite.addTest(BaseLevelCourseActualize("test_case_NotRealTime_ViewInformation_003"))
    suite.addTest(BaseLevelCourseActualize("test_case_NotRealTime_AssignHomework_004"))
    suite.addTest(BaseLevelCourseActualize("test_case_NotNetwork_ViewInformation_005"))
    suite.addTest(BaseLevelCourseActualize("test_case_NotNetwork_AssignHomework_006"))
    suite.addTest(BaseLevelCourseActualize("test_case_NotNetwork_CheckInformation_007"))

    suite.addTest(BaseLevelCourseStudy("test_case_RealTime_CourseInfo_001"))
    suite.addTest(BaseLevelCourseStudy("test_case_RealTime_Situation_002"))
    suite.addTest(BaseLevelCourseStudy("test_case_RealTime_DoHomework_003"))
    suite.addTest(BaseLevelCourseStudy("test_case_NotRealTime_CourseInfo_004"))
    suite.addTest(BaseLevelCourseStudy("test_case_NotRealTime_Situation_005"))
    suite.addTest(BaseLevelCourseStudy("test_case_NotRealTime_DoHomework_006"))
    suite.addTest(BaseLevelCourseStudy("test_case_NotNetwork_CourseInfo_007"))
    suite.addTest(BaseLevelCourseStudy("test_case_NotNetwork_Situation_008"))

    suite.addTest(BaseLevelCourseEvaluate("test_case_RealTime_ReviewHomework_001"))
    suite.addTest(BaseLevelCourseEvaluate("test_case_RealTime_Grade_002"))
    suite.addTest(BaseLevelCourseEvaluate("test_case_NotRealTime_ReviewHomework_003"))
    suite.addTest(BaseLevelCourseEvaluate("test_case_NotRealTime_Grade_004"))
    suite.addTest(BaseLevelCourseEvaluate("test_case_NotNetwork_Grade_005"))

    suite.addTest(BaseLevelCourseHourIdentify("test_case_RealTime_HourIdentify_001"))
    suite.addTest(BaseLevelCourseHourIdentify("test_case_NotRealTime_HourIdentify_002"))
    suite.addTest(BaseLevelCourseHourIdentify("test_case_NotNetwork_HourIdentify_003"))

    suite.addTest(BaseLevelRequirmentSurveySummary("test_case_BaseLevel_RequirmentSurveySummary_001"))

    currenttime = time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time()))
    filename = 'D:\\iTraining\\result\\reports\\'+currenttime+'results.html'
    fp=file(filename,'wb')
    runner=HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=u'基地级自动化测试报告',
            description=u'基地级自动化测试报告'
    )
    runner.run(suite)
    fp.close()