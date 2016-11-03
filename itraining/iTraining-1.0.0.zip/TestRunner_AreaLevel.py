# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, time, re, sys
import HTMLTestRunner
sys.path.append("..")
# print sys.path
from test_case.case_Login import TestCaseLogin
from test_case.case_Logout import TestCaseLogout
from test_case.case_AnnualPlanAdd import AnnualPlanAdd
from test_case.case_AnnualPlanManagement import AnnualPlanManagement
from test_case.case_CoursePlanAdd import CoursePlanAdd
from test_case.case_AreaLevelCoursePlanManagement import AreaLevelCoursePlanManagement
from test_case.case_AreaLevelCourseContentAdd import AreaLevelCourseContentAdd
from test_case.case_AreaLevelCourseRegistation import AreaLevelCourseRegistation
from test_case.case_AreaLevelCourseRegistationApproval import AreaLevelCourseRegistationApproval
from test_case.case_AreaLevelCourseActualize import AreaLevelCourseActualize
from test_case.case_AreaLevelCourseEvaluate import AreaLevelCourseEvaluate
from test_case.case_AreaLevelCourseStudy import AreaLevelCourseStudy
from test_case.case_AreaLevelCourseHourIdentify import AreaLevelCourseHourIdentify
from test_case.case_AreaLevelRequirmentSurveySummary import AreaLevelRequirmentSurveySummary
from test_case.case_AreaLevelCourseQuestionSurvey import AreaLevelCourseQuestionSurvey

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":

    suite = unittest.TestSuite()
    # suite.addTest(TestCaseLogin("test_case_login_001"))
    # suite.addTest(TestCaseLogin("test_case_login_002"))  

    # suite.addTest(AnnualPlanAdd("test_case_AnnualPlanAdd_AreaLevel_001"))
    # suite.addTest(AnnualPlanAdd("test_case_AnnualPlanAdd_FieldVerification_004"))

    # suite.addTest(AnnualPlanManagement("test_case_SearchAnnualPlan_001"))
    # suite.addTest(AnnualPlanManagement("test_case_PublishAnnualPlan_002"))
    # suite.addTest(AnnualPlanManagement("test_case_EditAnnualPlan_003"))
    # suite.addTest(AnnualPlanManagement("test_case_DeleteAnnualPlan_004"))

    # suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_AreaLevel_RealTime_001"))
    # suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_AreaLevel_NotRealTime_002"))
    # suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_AreaLevel_NotNetwork_003"))
    # suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_AreaLevel_ImportList_004"))
    # suite.addTest(CoursePlanAdd("test_case_CoursePlanAdd_FieldVerification_010"))

    # suite.addTest(AreaLevelCoursePlanManagement("test_case_AreaLevel_SearchCoursePlan_001"))
    # suite.addTest(AreaLevelCoursePlanManagement("test_case_AreaLevel_PublishCoursePlan_002"))
    # suite.addTest(AreaLevelCoursePlanManagement("test_case_AreaLevel_EditCoursePlan_003"))
    # suite.addTest(AreaLevelCoursePlanManagement("test_case_AreaLevel_DeleteCoursePlan_004"))

    # suite.addTest(AreaLevelCourseContentAdd("test_case_RealTime_AddCourseDesign_001"))
    # suite.addTest(AreaLevelCourseContentAdd("test_case_NotRealTime_AddCourseDesign_002"))
    # suite.addTest(AreaLevelCourseContentAdd("test_case_NotNetwork_AddCourseContent_003"))

    # suite.addTest(AreaLevelCourseRegistation("test_case_ForRigisterCriteria_001"))
    # suite.addTest(AreaLevelCourseRegistation("test_case_SearchCourse_Registation_002"))
    # suite.addTest(AreaLevelCourseRegistation("test_case_ViewCourse_Registation_003"))
    # suite.addTest(AreaLevelCourseRegistation("test_case_Comfirm_Registation_004"))
    # suite.addTest(AreaLevelCourseRegistation("test_case_Comfirm_Registation_005"))
    # suite.addTest(AreaLevelCourseRegistation("test_case_School_Recommend_006"))

    # suite.addTest(AreaLevelCourseRegistationApproval("test_case_AreaLevel_SearchApprovalRegistation_001"))
    # suite.addTest(AreaLevelCourseRegistationApproval("test_case_AreaLevel_ApproveRegistation_002"))
    # suite.addTest(AreaLevelCourseRegistationApproval("test_case_AreaLevel_ApproveRegistation_003"))
    # suite.addTest(AreaLevelCourseRegistationApproval("test_case_AreaLevel_ApproveRegistation_004"))
    
    # suite.addTest(AreaLevelCourseActualize("test_case_RealTime_ViewInformation_001"))
    # suite.addTest(AreaLevelCourseActualize("test_case_RealTime_AssignHomework_002"))
    # suite.addTest(AreaLevelCourseActualize("test_case_NotRealTime_ViewInformation_003"))
    # suite.addTest(AreaLevelCourseActualize("test_case_NotRealTime_AssignHomework_004"))
    # suite.addTest(AreaLevelCourseActualize("test_case_NotNetwork_ViewInformation_005"))
    # suite.addTest(AreaLevelCourseActualize("test_case_NotNetwork_AssignHomework_006"))
    # suite.addTest(AreaLevelCourseActualize("test_case_NotNetwork_CheckInformation_007"))

    # suite.addTest(AreaLevelCourseStudy("test_case_RealTime_CourseInfo_001"))
    # suite.addTest(AreaLevelCourseStudy("test_case_RealTime_Situation_002"))
    # suite.addTest(AreaLevelCourseStudy("test_case_RealTime_DoHomework_003"))
    # suite.addTest(AreaLevelCourseStudy("test_case_NotRealTime_CourseInfo_004"))
    # suite.addTest(AreaLevelCourseStudy("test_case_NotRealTime_Situation_005"))
    # suite.addTest(AreaLevelCourseStudy("test_case_NotRealTime_DoHomework_006"))
    # suite.addTest(AreaLevelCourseStudy("test_case_NotNetwork_CourseInfo_007"))
    # suite.addTest(AreaLevelCourseStudy("test_case_NotNetwork_Situation_008"))

    # suite.addTest(AreaLevelCourseEvaluate("test_case_RealTime_ReviewHomework_001"))
    # suite.addTest(AreaLevelCourseEvaluate("test_case_RealTime_Grade_002"))
    # suite.addTest(AreaLevelCourseEvaluate("test_case_NotRealTime_ReviewHomework_003"))
    suite.addTest(AreaLevelCourseEvaluate("test_case_NotRealTime_Grade_004"))
    # suite.addTest(AreaLevelCourseEvaluate("test_case_NotNetwork_Grade_005"))

    # suite.addTest(AreaLevelCourseHourIdentify("test_case_RealTime_HourIdentify_001"))
    suite.addTest(AreaLevelCourseHourIdentify("test_case_NotRealTime_HourIdentify_002"))
    # suite.addTest(AreaLevelCourseHourIdentify("test_case_NotNetwork_HourIdentify_003"))
    
    suite.addTest(AreaLevelRequirmentSurveySummary("test_case_AreaLevel_RequirmentSurveySummary_001"))

    # suite.addTest(AreaLevelCourseQuestionSurvey("test_case_Add_QuestionSurvey_001"))
    # suite.addTest(AreaLevelCourseQuestionSurvey("test_case_Submit_QuestionSurvey_002"))
    # suite.addTest(AreaLevelCourseQuestionSurvey("test_case_Result_QuestionSurvey_003"))   

    currenttime = time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time()))
    filename = 'D:\\iTraining\\result\\reports\\'+currenttime+'results.html'
    fp=file(filename,'wb')
    runner=HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=u'区级自动化测试报告',
            description=u'区级自动化测试报告'
    )
    runner.run(suite)
    fp.close()