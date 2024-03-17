set -e

mongosh <<!
    use ad_publish

    db.createUser({
      user: '$AD_PUBLISH_USER',
      pwd: '$AD_PUBLISH_PASSWORD',
      roles: [{ role: 'readWrite', db: 'ad_publish' }],
    });
!
