#ifndef BBAMI_H_
#define BBAMI_H_

#include <sys/cdefs.h>

__BEGIN_DECLS

#define BBAMI_API_VERSION 1

#define DEFAULT_MANIFEST_PATH 0

typedef enum {
    AUTHOR,
    ARCHIVE_CREATED_BY,
    ARCHIVE_MANIFEST_VERSION,

    APPLICATION_NAME,
    APPLICATION_DESCRIPTION,
    APPLICATION_VERSION,
    APPLICATION_ID,
    APPLICATION_VERSION_ID,
    APPLICATION_DEVELOPMENT_MODE,
    APPLICATION_REQUIRES_SYSTEM,
    APPLICATION_CATEGORY,

    PACKAGE_TYPE,
    PACKAGE_AUTHOR,
    PACKAGE_NAME,
    PACKAGE_VERSION,
    PACKAGE_ARCHITECTURE,
    PACKAGE_AUTHOR_CERTIFICATE_HASH,
    PACKAGE_AUTHOR_ID,
    PACKAGE_ID,
    PACKAGE_VERSION_ID,

    ENTRY_POINT,
    ENTRY_POINT_NAME,
    ENTRY_POINT_TYPE,
    ENTRY_POINT_ICON,
    ENTRY_POINT_SPLASH_SCREEN,
    ENTRY_POINT_ORIENTATION,
    ENTRY_POINT_USER_ACTIONS,
    ENTRY_POINT_SYSTEM_ACTIONS,

    ARCHIVE_ASSET_NAME,
    ARCHIVE_ASSET_SHA_512_DIGEST
} bbami_attribute_id;

struct bbami_info;
typedef struct bbami_info * bbami_info_ptr;

/** @brief Initializes BlackBerry application meta information context
 *
 * Initializes BlackBerry application meta information using
 * the provided manifest file path.
 * One can use DEFAULT_MANIFEST_PATH for manifest file path to
 * get information from meta information files in application
 * sandbox directory (from HOME environment variable).
 *
 * @param api_version API version. Please use BBAMI_API_VERSION constant.
 * @param manifest_path File path to read manifest meta information from.
 *                      One could use DEFAULT_MANIFEST_PATH as the default,
 *                      in this case the file will be read from the current
 *                      application sandbox
 * @param info Initialized BlackBerry application meta information context is
 *             returned to the caller using this parameter
 * @return 0 on success and negative errno value on failure.
 */
int bbami_init(int api_version,
               char * manifest_path,
               bbami_info_ptr * info);

/** @brief Get number of values for the specified attribute Id
 *
 * Retrieves the number of values existing for the provided attribute Id.
 *
 * @param info BlackBerry application meta information context
 * @param attribute_id Attribute Id, see bbami_attribute_id enumeration
 * @param count Pointer to an integer that will contain the number of values
 * @return 0 on success and negative errno value on failure.
 */
int bbami_value_count(bbami_info_ptr info,
                      bbami_attribute_id attribute_id,
                      int * count);

/** @brief Get the value for the specified attribute Id
 *
 * Retrieves the value for the provided attribute Id.
 * The function will allocate the memory that the caller should free.
 *
 * @param info BlackBerry application meta information context
 * @param attribute_id Attribute Id, see bbami_attribute_id enumeration
 * @param value Pointer to a string that will contain the allocated
 *              copy of the value for the given attribute Id.
 *              The memory should be freed when it is no longer needed
 * @return 0 on success and negative errno value on failure.
 */
int bbami_query(bbami_info_ptr info,
                bbami_attribute_id attribute_id,
                char ** value);

/** @brief Get the Nth value for the specified attribute Id
 *
 * Retrieves the value for the provided attribute Id and index.
 * The function will allocate the memory that the caller should free.
 *
 * @param info BlackBerry application meta information context
 * @param attribute_id Attribute Id, see bbami_attribute_id enumeration
 * @param index value sequential index, starting from 0
 *              One could call bbami_value_count to get the total
 *              number of values for the specified attribute Id.
 * @param value Pointer to a string that will contain the allocated
 *              copy of the value for the given attribute Id.
 *              The memory should be freed when it is no longer needed
 * @return 0 on success and negative errno value on failure.
 */
int bbami_query_by_index(bbami_info_ptr info,
                         bbami_attribute_id attribute_id,
                         int index,
                         char ** value);

/** @brief Disposes the BlackBerry application meta information context
 *
 * Call this function to dispose of BlackBerry application meta information
 * context and free resources.
 *
 * @param info BlackBerry application meta information context
 * @param attribute_id Attribute Id, see bbami_attribute_id enumeration
 * @param count Pointer to an integer that will contain the number of values
 * @return 0 on success and negative errno value on failure.
 */
int bbami_done(bbami_info_ptr info);

__END_DECLS

#endif /* BBAMI_H_ */
