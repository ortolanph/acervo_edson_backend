from datetime import datetime

from flask_restx import Namespace, Resource

from infra import db

system_info_ns = Namespace(
    'system_info',
    description='Useful system information')


@system_info_ns.route("/health")
class SystemHealth(Resource):

    @system_info_ns.doc('health_check')
    def get(self):
        """Health check endpoint"""
        return {
            'status': 'OK',
            'timestamp': str(datetime.now()),
            'service': 'Acervus',
            'database_status': 'OK' if db else 'KO'
        }


@system_info_ns.route("/version")
class SystemVersion(Resource):

    @system_info_ns.doc('system_version')
    def get(self):
        """System Version"""
        return {
            'project_name': 'Acervus',
            'version': '0.0.0',
            'details': {
                'major': 0,
                'minor': 0,
                'fix': 0
            }
        }
